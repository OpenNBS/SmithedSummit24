from pathlib import Path

from beet import Context, Sound, SoundConfig

EXTRA_NOTES = {
    "block.note_block.banjo_-1": "banjo_-1.ogg",
    "block.note_block.banjo_1": "banjo_1.ogg",
    "block.note_block.basedrum_-1": "basedrum_-1.ogg",
    "block.note_block.basedrum_1": "basedrum_1.ogg",
    "block.note_block.bass_-1": "bassattack_-1.ogg",
    "block.note_block.bass_1": "bassattack_1.ogg",
    "block.note_block.bell_-1": "bell_-1.ogg",
    "block.note_block.bell_1": "bell_1.ogg",
    "block.note_block.bit_-1": "bit_-1.ogg",
    "block.note_block.bit_1": "bit_1.ogg",
    "block.note_block.cow_bell_-1": "cow_bell_-1.ogg",
    "block.note_block.cow_bell_1": "cow_bell_1.ogg",
    "block.note_block.didgeridoo_-1": "didgeridoo_-1.ogg",
    "block.note_block.didgeridoo_1": "didgeridoo_1.ogg",
    "block.note_block.flute_-1": "flute_-1.ogg",
    "block.note_block.flute_1": "flute_1.ogg",
    "block.note_block.guitar_-1": "guitar_-1.ogg",
    "block.note_block.guitar_1": "guitar_1.ogg",
    "block.note_block.harp_-1": "harp_-1.ogg",
    "block.note_block.harp_1": "harp_1.ogg",
    "block.note_block.hat_-1": "hat_-1.ogg",
    "block.note_block.hat_1": "hat_1.ogg",
    "block.note_block.chime_-1": "icechime_-1.ogg",
    "block.note_block.chime_1": "icechime_1.ogg",
    "block.note_block.iron_xylophone_-1": "iron_xylophone_-1.ogg",
    "block.note_block.iron_xylophone_1": "iron_xylophone_1.ogg",
    "block.note_block.pling_-1": "pling_-1.ogg",
    "block.note_block.pling_1": "pling_1.ogg",
    "block.note_block.snare_-1": "snare_-1.ogg",
    "block.note_block.snare_1": "snare_1.ogg",
    "block.note_block.xylophone_-1": "xylobone_-1.ogg",
    "block.note_block.xylophone_1": "xylobone_1.ogg",
}


def beet_default(ctx: Context):
    sound_config = {}

    for instrument in ctx.meta["instruments"]:
        sound_path = EXTRA_NOTES.get(instrument)
        if sound_path is not None:
            instrument_path = instrument.replace(".", "/")
            ctx.assets["minecraft"].sounds[instrument_path] = Sound(
                (Path("sounds") / sound_path).read_bytes(),
                event=instrument,
                subtitle="subtitles.block.note_block.note",
            )

            sound_config[instrument] = {
                "sounds": [instrument_path],
                "subtitle": "subtitles.block.note_block.note",
            }

        elif instrument is not None and not instrument.startswith("block.note_block."):
            instrument_resource = instrument.replace("/", "_")

            sound_config[instrument_resource] = {
                "sounds": [instrument],
                "subtitle": "subtitles.block.note_block.note",
            }

    ctx.assets["minecraft"].sound_config = SoundConfig(sound_config)
