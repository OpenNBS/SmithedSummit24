from fnmatch import fnmatch

from beet import Context, Model, Texture, TextureMcmeta
from PIL import Image

models = [
    "nbw_block",
    "nbw_text",
    "scroll_panel",
    "flat_note_block",
    "gramophone_base",
    "gramophone",
    "record_player",
    "speakers",
    "headphones",
    "records_double",
    "records_triple",
    "piano",
    "guitar",
    "open_sign",
]

emissive_textures = ["scroll_panel_*", "note*"]

no_shade_textures = ["nbw_*"]

EMISSIVE_ALPHA = 254
NO_SHADE_ALPHA = 253

CMD_OFFSET = 48184


def generate_model_predicates(parent: str, models: list[str]) -> Model:
    return Model(
        {
            "parent": parent,
            "overrides": [
                {
                    "predicate": {"custom_model_data": str(CMD_OFFSET) + str(cmd)},
                    "model": f"nbs:{model}",
                }
                for cmd, model in enumerate(models)
            ],
        }
    )


def generate_scrolling_texture(img: Image.Image, scroll_factor: int = 4) -> Texture:
    width, height = img.size
    tile_size = img.height

    frames = []

    # Grow the image to the left to allow for scrolling
    src = Image.new("RGBA", (width + tile_size, height), (0, 0, 0, 0))
    src.paste(img, (tile_size, 0))

    for x in range(-tile_size, width + tile_size, scroll_factor):
        frame = img.crop((x, 0, x + tile_size, height))
        frames.append(frame)

    output = Image.new("RGBA", (tile_size, height * len(frames)), (0, 0, 0, 0))

    for i, frame in enumerate(frames):
        output.paste(frame, (0, i * height))

    return Texture(output)


def generate_scrolling_mcmetas(
    texture: Texture, scroll_factor: int = 4, panel_count: int = 5
) -> list[TextureMcmeta]:
    mcmetas = []

    tile_size, height = texture.image.size
    frames = height // tile_size

    # This is how many frames it takes to reach the second slice of the panel
    frames_per_slice = tile_size // scroll_factor

    for i in range(panel_count):
        start_frame = i * frames_per_slice
        mcmeta = {
            "animation": {
                "interpolate": False,
                "frametime": 1,
                "frames": [
                    i % frames for i in range(start_frame, start_frame + frames)
                ],
            }
        }
        mcmetas.append(TextureMcmeta(mcmeta))

    return mcmetas


def generate_scrolling_animation(ctx: Context) -> None:
    panel_texture = ctx.assets.textures["nbs:block/nbw_32x"]
    texture = generate_scrolling_texture(panel_texture.image)
    mcmetas = generate_scrolling_mcmetas(texture)
    for i, mcmeta in enumerate(mcmetas, start=1):
        ctx.assets.textures[f"nbs:block/scroll_panel_{i}"] = texture
        ctx.assets.textures_mcmeta[f"nbs:block/scroll_panel_{i}"] = mcmeta
    del ctx.assets.textures["nbs:block/nbw_32x"]


def apply_emissive_textures(ctx: Context) -> None:
    for name, texture in ctx.assets.textures.items():
        name = name.split("/")[-1]
        if any(fnmatch(name, pattern) for pattern in emissive_textures):
            if texture.image.mode != "RGBA":
                texture.image = texture.image.convert("RGBA")
            texture.image.putalpha(EMISSIVE_ALPHA)
        if any(fnmatch(name, pattern) for pattern in no_shade_textures):
            if texture.image.mode != "RGBA":
                texture.image = texture.image.convert("RGBA")
            texture.image.putalpha(NO_SHADE_ALPHA)


def create_note_models(ctx: Context) -> None:
    note_variants = filter(
        lambda name: name.startswith("nbs:block/note"), ctx.assets.textures
    )

    global models
    for texture in note_variants:
        note_model = Model(
            {
                "parent": "nbs:note_base",
                "textures": {"0": texture},
            }
        )
        filename = texture.split("/")[-1]
        ctx.assets.models[f"nbs:{filename}"] = note_model
        models.append(filename)


def beet_default(ctx: Context):
    create_note_models(ctx)

    ctx.assets["minecraft:item/note_block"] = generate_model_predicates(
        "block/note_block", models
    )
    generate_scrolling_animation(ctx)
    apply_emissive_textures(ctx)
