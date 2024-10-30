from fnmatch import fnmatch

from beet import Context, Model, Texture, TextureMcmeta
from PIL import Image, ImageChops

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
    "wall_art",
    "balloon_nbs",
]

models_cmd = {model: i for i, model in enumerate(models)}

emissive_textures = ["scroll_panel_*", "note_sign_*", "monitor_*", "open_sign"]

no_shade_textures = ["nbw_*"]

EMISSIVE_ALPHA = 254
NO_SHADE_ALPHA = 253

CMD_OFFSET = 48184

MONITOR_TEXTURE_SIZE = 512


def generate_model_predicates(parent: str, models: list[str] | dict[str, int]) -> Model:
    if isinstance(models, list):
        models_cmd = {model: cmd for cmd, model in enumerate(models)}
    else:
        models_cmd = models

    return Model(
        {
            "parent": parent,
            "overrides": [
                {
                    "predicate": {"custom_model_data": CMD_OFFSET + cmd + 1},
                    "model": f"nbs:{model}",
                }
                for model, cmd in models_cmd.items()
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
    def multiply_alpha(img: Image.Image, alpha: int) -> Image.Image:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        # set the alpha value to the desired value where it is not 0
        mask = Image.eval(img.split()[3], lambda a: 0 if a == 0 else alpha)
        img.putalpha(mask)
        return img

    for name, texture in ctx.assets.textures.items():
        name = name.split("/")[-1]
        if any(fnmatch(name, pattern) for pattern in emissive_textures):
            texture.image = multiply_alpha(texture.image, EMISSIVE_ALPHA)
        if any(fnmatch(name, pattern) for pattern in no_shade_textures):
            texture.image = multiply_alpha(texture.image, NO_SHADE_ALPHA)


def create_note_models(ctx: Context) -> None:
    note_variants = filter(
        lambda name: name.startswith("nbs:block/note_sign_"), ctx.assets.textures
    )

    global models
    for i, texture in enumerate(note_variants):
        note_model = Model(
            {
                "parent": "nbs:note_base",
                "textures": {"0": texture},
            }
        )
        filename = texture.split("/")[-1]
        ctx.assets.models[f"nbs:{filename}"] = note_model
        models_cmd[filename] = i + 100


def create_monitor_models(ctx: Context) -> None:
    monitor_variants = filter(
        lambda name: name.startswith("nbs:block/monitor_"), ctx.assets.textures
    )

    global models
    for texture in monitor_variants:
        size = MONITOR_TEXTURE_SIZE
        # The monitor is 12x10 pixels. We stretch the image to a 512x512 texture
        src_img: Image.Image = ctx.assets.textures[texture].image
        resized_img = src_img.resize((size, size), Image.Resampling.LANCZOS)
        ctx.assets.textures[texture] = Texture(resized_img)

    for i in range(6):
        texture = f"nbs:block/monitor_{i}"
        if texture not in ctx.assets.textures:
            texture = "nbs:block/monitor_0"
        monitor_model = Model(
            {
                "parent": "nbs:monitor",
                "textures": {"content": f"nbs:block/monitor_{i}"},
            }
        )
        filename = texture.split("/")[-1]
        ctx.assets.models[f"nbs:{filename}"] = monitor_model

        models_cmd[f"monitor_{i}"] = i + 200


def apply_alpha(img: Image.Image, alpha_texture: Image.Image) -> Image.Image:
    def get_alpha_from_level(level: int) -> int:
        if level < 64:
            return 8
        elif level < 128:
            return 7
        elif level < 192:
            return 6
        else:
            return 5

    img = img.convert("RGBA")
    alpha_texture = alpha_texture.convert("L")
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            if not isinstance(pixel, tuple):
                raise ValueError(f"Expected RGBA pixel, got {pixel}")
            r, g, b, a = pixel
            if a == 0:
                continue
            level = alpha_texture.getpixel((x, y))
            if not isinstance(level, int):
                raise ValueError(f"Alpha mask image must be in grayscale (L) mode")
            alpha = get_alpha_from_level(level)
            img.putpixel((x, y), (r, g, b, alpha))
    return img


def create_balloon_models(ctx: Context) -> None:

    # Apply alpha to the note block balloon texture
    balloon_texture = ctx.assets.textures["nbs:item/balloons/balloon_nbs"].image
    alpha_texture = ctx.assets.textures["nbs:item/balloons/balloon_nbs_alpha"].image
    balloon_texture = apply_alpha(balloon_texture, alpha_texture)
    ctx.assets.textures["nbs:item/balloons/balloon_nbs"] = Texture(balloon_texture)
    del ctx.assets.textures["nbs:item/balloons/balloon_nbs_alpha"]

    balloon_variants = filter(
        lambda name: name.startswith("nbs:item/balloons/balloon_note"),
        ctx.assets.textures,
    )

    for i, texture in enumerate(balloon_variants):
        if "alpha" in texture:
            continue

        # Create models for each balloon variant
        balloon_model = Model(
            {
                "parent": "nbs:balloon_note_base",
                "textures": {"balloon": texture},
            }
        )
        filename = texture.split("/")[-1]
        ctx.assets.models[f"nbs:{filename}"] = balloon_model
        models_cmd[filename] = i + 300

        # Apply alpha to the balloon texture
        balloon_texture = ctx.assets.textures[texture].image
        alpha_texture = ctx.assets.textures[
            "nbs:item/balloons/balloon_note_alpha"
        ].image
        balloon_texture = apply_alpha(balloon_texture, alpha_texture)
        ctx.assets.textures[texture] = Texture(balloon_texture)
    del ctx.assets.textures["nbs:item/balloons/balloon_note_alpha"]


def beet_default(ctx: Context):
    create_note_models(ctx)
    create_monitor_models(ctx)
    create_balloon_models(ctx)

    ctx.assets["minecraft:item/note_block"] = generate_model_predicates(
        "block/note_block", models_cmd
    )
    ctx.assets["minecraft:item/carved_pumpkin"] = generate_model_predicates(
        "block/carved_pumpkin", ["headphones"]
    )

    generate_scrolling_animation(ctx)
    apply_emissive_textures(ctx)
