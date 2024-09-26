import os
from pathlib import Path

import pynbs
from beet import Context, Function

from pigstep import pigstep


def beet_default(ctx: Context) -> None:

    temp_songs_path = Path("songs", ".temp")
    if not os.path.exists(temp_songs_path):
        os.makedirs(temp_songs_path)

    # Patch NBS file to work with pigstep's quirks (fix it there eventually!)

    processed_song_paths = []

    for file in Path("songs").glob("*.nbs"):
        song = pynbs.read(file)

        # Set instrument name to sound event name (pigstep uses the sound file field as the sound event)
        for ins in song.instruments:
            new_ins = pynbs.Instrument(
                id=ins.id,
                name=ins.name,
                file=ins.name,
                pitch=ins.pitch,
                press_key=ins.press_key,
            )
            song.instruments[ins.id] = new_ins

        # Quantize notes to nearest tick (pigstep always exports at 20 t/s)
        # Remove notes outside the 6-octave range
        new_notes = []
        for tick, chord in song:
            new_tick = round(tick * 20 / song.header.tempo)
            for note in chord:
                note.tick = new_tick
                if 9 <= note.key <= 81:
                    new_notes.append(note)
        song.notes = new_notes

        # Ensure that there are as many layers as the last layer with a note
        max_layer = max(note.layer for note in song.notes)
        while len(song.layers) <= max_layer:
            song.layers.append(pynbs.Layer(id=len(song.layers)))

        # Make sure instrument paths are valid
        for instrument in song.instruments:
            instrument.file = instrument.file.lower().replace(" ", "_")

        # Save song to a temp file
        filename = Path(temp_songs_path, file.name)
        song.save(filename)

        processed_song_paths.append(str(filename))
        print("Exported song", file.name)

    ctx.generate("tick", render=Function(source_path="global_tick.mcfunction"))

    ctx.require(
        pigstep(
            load=processed_song_paths,
            source="record",
            templates={
                "tick": "tick.mcfunction",
            },
        )
    )

    print("Done!")
