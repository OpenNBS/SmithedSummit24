__all__ = [
    "Note",
    "load_nbs",
    "get_pitch",
]


import math
from dataclasses import dataclass
from typing import Any, Iterator, List, Tuple

import pynbs
from beet.core.utils import FileSystemPath

NBS_DEFAULT_INSTRUMENTS = [
    "block.note_block.harp",
    "block.note_block.bass",
    "block.note_block.basedrum",
    "block.note_block.snare",
    "block.note_block.hat",
    "block.note_block.guitar",
    "block.note_block.flute",
    "block.note_block.bell",
    "block.note_block.chime",
    "block.note_block.xylophone",
    "block.note_block.iron_xylophone",
    "block.note_block.cow_bell",
    "block.note_block.didgeridoo",
    "block.note_block.bit",
    "block.note_block.banjo",
    "block.note_block.pling",
]

octaves = {
    "harp": 0,
    "bass": -2,
    "basedrum": -1,
    "snare": 1,
    "hat": 0,
    "guitar": -1,
    "flute": 1,
    "bell": 2,
    "chime": 2,
    "xylophone": 2,
    "iron_xylophone": 0,
    "cow_bell": 0,
    "didgeridoo": -2,
    "bit": 0,
    "banjo": 0,
    "pling": 0,
}


@dataclass
class Note:
    """Represents a note produced by a /playsound command."""

    instrument: str = "block.note_block.harp"
    position: str = "^ ^ ^"
    volume: float = 1
    radius: float = 16
    pitch: float = 1

    def play(self, player: str = "@s", source: str = "record") -> str:
        """Return the /playsound command to play the note for the given player."""
        return f"playsound {self.instrument} {source} @a[distance=..{self.radius}] {self.position} {self.volume} {self.pitch}"


def load_nbs(filename: FileSystemPath) -> Iterator[Tuple[int, List["Note"]]]:
    """Yield all the notes from the given nbs file."""

    song = pynbs.read(filename)

    # Quantize notes to nearest tick (pigstep always exports at 20 t/s)
    # Remove notes outside the 6-octave range
    new_notes = []
    for tick, chord in song:
        new_tick = round(tick * 20 / song.header.tempo)
        for note in chord:
            note.tick = new_tick
            note_pitch = get_pitch(note)
            is_custom_instrument = note.instrument >= song.header.default_instruments
            is_2_octave = 33 <= note_pitch <= 57
            is_6_octave = 9 <= note_pitch <= 81

            if is_custom_instrument and not is_2_octave:
                # print(
                #    f"Warning: Custom instrument out of 2-octave range at {note.tick},{note.layer}: {note_pitch}"
                # )
                continue

            if not is_custom_instrument and not is_6_octave:
                # print(
                #    f"Warning: Vanilla instrument out of 6-octave range at {note.tick},{note.layer}: {note_pitch}"
                # )
                continue

            new_notes.append(note)

    # song.notes = new_notes

    # Ensure that there are as many layers as the last layer with a note
    max_layer = max(note.layer for note in song.notes)
    while len(song.layers) <= max_layer:
        song.layers.append(pynbs.Layer(id=len(song.layers)))

    # Make sure instrument paths are valid
    for instrument in song.instruments:
        instrument.file = instrument.file.lower().replace(" ", "_")

    sounds = NBS_DEFAULT_INSTRUMENTS + [
        instrument.file.replace("minecraft/", "").replace(".ogg", "")
        for instrument in song.instruments
    ]

    def get_note(note: Any) -> Note:
        """Get a /playsound note from a given nbs note."""

        layer = song.layers[note.layer]

        sound = sounds[note.instrument].replace("/", "_")
        pitch = note.key + (note.pitch / 100)
        octave_suffix = "_-1" if pitch < 33 else "_1" if pitch > 57 else ""
        source = f"{sound}{octave_suffix}"

        layer_volume = layer.volume / 100
        note_volume = note.velocity / 100
        global_volume = 1
        instrument = sound.split(".")[-1]
        volume = layer_volume * note_volume * global_volume

        radius = 9 + get_rolloff_factor(pitch, instrument)

        pitch = get_pitch(note)

        position = "^ ^ ^"  # get_panning(note, layer)

        return Note(source, position, volume, radius, pitch)

    for tick, chord in song:
        yield tick, [get_note(note) for note in chord]


def get_panning(note: Any, layer: Any) -> str:
    """Get panning for a given nbs note."""
    if layer.panning == 0:
        pan = note.panning
    else:
        pan = (layer.panning + note.panning) / 2
    pan /= 100
    return "^ ^ ^" + f"{pan * 4}"


def get_pitch(note: Any) -> float:
    """Get pitch for a given nbs note."""
    key = note.key + note.pitch / 100

    if key < 33:
        key -= 9
    elif key > 57:
        key -= 57
    else:
        key -= 33

    return 2 ** (key / 12) / 2


def sigmoid(x: float, slope: float = 1, offset: float = 0, scale: float = 1) -> float:
    return (1 / (1 + math.exp(-x * slope)) + offset) * scale


def rolloff_curve(x: float) -> float:
    # slope  = -6   -> make curve steeper towards the center and mirror it in the x axis
    # offset = -0.5 -> move the curve down so its center is at y=0
    # scale  = 6    -> scale the curve so it goes from -3 to 3 as x approaches +/-inf

    # see: https://www.desmos.com/calculator/roidl8wnxl

    return sigmoid(x, -6, -0.5, 6)


def get_rolloff_factor(pitch: float, instrument: str) -> float:
    # Calculate true pitch taking into account each instrument's octave offset
    real_pitch = pitch + 12 * octaves.get(instrument, 1)
    # 45 is the middle point (33-57) of the 6-octave range, where the rolloff factor should be 0
    factor = (real_pitch - 45) / (45 - 8)
    return rolloff_curve(factor)
