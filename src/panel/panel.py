import json
from pathlib import Path

from beet import Advancement, Context, Model, SoundConfig, Texture
from PIL import Image, ImageEnhance

from src.model import apply_emissive_textures, generate_model_predicates

models = ["nbs:nbw_block", "nbs:nbw_text", "nbs:nbw_block_dark", "nbs:nbw_text_dark"]
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

    # Lever interaction
    ctx.data["nbs:lever_interaction"] = Advancement(
        {
            "criteria": {
                "example": {
                    "trigger": "minecraft:default_block_use",
                    "conditions": {
                        "location": [
                            {
                                "condition": "minecraft:location_check",
                                "predicate": {"block": {"blocks": "minecraft:lever"}},
                            }
                        ]
                    },
                }
            },
            "rewards": {"function": "nbs:panel/lever_interaction"},
        }
    )

    # Create dark model
    for texture in textures:
        original_img = ctx.assets.textures[texture].image.convert("RGBA")
        frame = original_img.crop((0, 0, original_img.width, original_img.width))
        brightness_effect = ImageEnhance.Brightness(frame)
        ctx.assets.textures[f"{texture}_dark"] = Texture(
            brightness_effect.enhance(0.05)
        )

    ctx.assets.models["nbs:nbw_block_dark"] = Model(
        {
            "parent": "nbs:nbw_block",
            "textures": {
                "0": "nbs:block/nbw_left_dark",
                "1": "nbs:block/nbw_right_dark",
                "2": "nbs:block/nbw_top_dark",
            },
        }
    )

    ctx.assets.models["nbs:nbw_text_dark"] = Model(
        {
            "parent": "nbs:nbw_text",
            "textures": {
                "2": "nbs:block/nbw_text_dark",
            },
        }
    )

    # Generate model predicates
    ctx.assets["minecraft:item/note_block"] = generate_model_predicates(
        "block/note_block", [models.replace("nbs:", "") for models in models]
    )

    apply_emissive_textures(ctx)
