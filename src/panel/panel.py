import json
from pathlib import Path

from beet import Context, SoundConfig, Texture
from PIL import Image

from src.model import apply_emissive_textures, generate_model_predicates

models = ["nbs:nbw_block", "nbs:nbw_text"]
textures = [
    "nbs:block/nbw_left",
    "nbs:block/nbw_right",
    "nbs:block/nbw_top",
    "nbs:block/nbw_text",
]


def beet_default(ctx: Context):
    textures_to_delete = []
    for texture in ctx.assets.textures:
        if texture not in textures:
            textures_to_delete.append(texture)
    for texture in textures_to_delete:
        del ctx.assets.textures[texture]
        if texture in ctx.assets.textures_mcmeta:
            del ctx.assets.textures_mcmeta[texture]

    models_to_delete = []
    for model in ctx.assets.models:
        if model not in models:
            models_to_delete.append(model)
    for model in models_to_delete:
        del ctx.assets.models[model]

    ctx.assets["minecraft:item/note_block"] = generate_model_predicates(
        "block/note_block", [models.replace("nbs:", "") for models in models]
    )

    # Remove lightning sound
    ctx.assets["minecraft"].sound_config.merge(  # type: ignore
        SoundConfig(
            {
                "entity.lightning_bolt.thunder": {
                    "sounds": [],
                    "replace": True,
                }
            }
        )
    )

    apply_emissive_textures(ctx)
