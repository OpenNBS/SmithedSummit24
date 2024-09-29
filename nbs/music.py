import os
from pathlib import Path

import pynbs
from beet import Context, Function

from pigstep import pigstep

# from beet.contrib.vanilla import Vanilla


def get_pitch(note: pynbs.Note) -> float:
    return note.key + note.pitch / 100


def beet_default(ctx: Context) -> None:

    # Inject vanilla assets
    # vanilla = ctx.inject(Vanilla)
    # vanilla.mount("assets/minecraft/sounds")

    temp_songs_path = Path("songs", ".temp")
    if not os.path.exists(temp_songs_path):
        os.makedirs(temp_songs_path)

    # Patch NBS file to work with pigstep's quirks (fix it there eventually!)

    processed_song_paths = []

    for file in Path("songs").glob("*.nbs"):
        song = pynbs.read(file)

        # Quantize notes to nearest tick (pigstep always exports at 20 t/s)
        # Remove notes outside the 6-octave range
        new_notes = []
        for tick, chord in song:
            new_tick = round(tick * 20 / song.header.tempo)
            for note in chord:
                note.tick = new_tick
                note_pitch = get_pitch(note)
                is_custom_instrument = (
                    note.instrument >= song.header.default_instruments
                )
                is_2_octave = 33 <= note_pitch <= 57
                is_6_octave = 9 <= note_pitch <= 81

                if is_custom_instrument and not is_2_octave:
                    print(
                        f"Warning: Custom instrument out of 2-octave range at {note.tick},{note.layer}: {note_pitch}"
                    )
                    continue

                if not is_custom_instrument and not is_6_octave:
                    print(
                        f"Warning: Vanilla instrument out of 6-octave range at {note.tick},{note.layer}: {note_pitch}"
                    )
                    continue

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
