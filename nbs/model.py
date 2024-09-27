from beet import Context, Model, Texture, TextureMcmeta
from PIL import Image

models = [
    "nbw_block",
    "nbw_text",
    "scroll_panel",
    "note_block_flat",
    "note",
    "gramophone_base",
    "gramophone",
    "record_player",
    "speakers",
    "headphones",
]


def generate_model_predicates(parent: str, models: list[str]) -> Model:
    return Model(
        {
            "parent": parent,
            "overrides": [
                {"predicate": {"custom_model_data": cmd + 1}, "model": f"nbs:{model}"}
                for cmd, model in enumerate(models)
            ],
        }
    )


def generate_scrolling_texture(img: Image.Image, scroll_factor: int = 4) -> Texture:
    width, height = img.size
    tile_size = img.height

    frames = []

    for x in range(0, width + tile_size, scroll_factor):
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


def beet_default(ctx: Context):
    ctx.assets["minecraft:item/note_block"] = generate_model_predicates(
        "block/note_block", models
    )

    generate_scrolling_animation(ctx)
