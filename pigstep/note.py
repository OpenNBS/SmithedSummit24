__all__ = [
    "Note",
    "load_nbs",
    "get_pitch",
]


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
    pitch: float = 1

    def play(self, player: str = "@s", source: str = "record") -> str:
        """Return the /playsound command to play the note for the given player."""
        return f"playsound {self.instrument} {source} {player} {self.position} {self.volume} {self.pitch}"


def load_nbs(filename: FileSystemPath) -> Iterator[Tuple[int, List["Note"]]]:
    """Yield all the notes from the given nbs file."""
    song = pynbs.read(filename)
    sounds = NBS_DEFAULT_INSTRUMENTS + [
        instrument.file for instrument in song.instruments
    ]

    pitch = lambda note: note.key + (note.pitch / 100)

    for tick, chord in song:
        yield tick, [
            Note(
                instrument=sounds[note.instrument]
                + ("_-1" if pitch(note) < 33 else "_1" if pitch(note) > 57 else ""),
                volume=(song.layers[note.layer].volume / 100)
                * (note.velocity / 100)
                * 8
                * get_rolloff_factor(
                    pitch(note), sounds[note.instrument].split(".")[-1]
                ),
                # make bass notes propagate further
                pitch=get_pitch(
                    note,
                ),
                position=get_panning(note, song.layers[note.layer]),
            )
            for note in chord
        ]


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


def get_rolloff_factor(pitch: Any, instrument: str) -> float:
    # Calculate true pitch taking into eaccount each instrument's octave offset
    real_pitch = pitch + 12 * octaves.get(instrument, 1)
    return 1 / (real_pitch / 45 + 1)
