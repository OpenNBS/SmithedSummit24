from beet import Context, Model

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


def beet_default(ctx: Context):
    ctx.assets["minecraft:item/note_block"] = generate_model_predicates(
        "block/note_block", models
    )
