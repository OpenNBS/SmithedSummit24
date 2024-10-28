from dataclasses import dataclass

from beet import Advancement, Context, Function


@dataclass
class Interaction:
    id: str
    tag_name: str
    function_left: str | None = None
    function_right: str | None = None


interactions = [
    Interaction(
        id="headphones",
        tag_name="nbs_headphone_collectible",
    ),
    Interaction(
        id="nbs_link",
        tag_name="nbs_nbs_link",
    ),
    Interaction(
        id="nbw_link",
        tag_name="nbs_nbw_link",
    ),
]


def generate_advancement(ctx: Context, interaction: Interaction):

    def get_advancement(click: str, function: str) -> Advancement:
        criteria = (
            "player_hurt_entity" if click == "left" else "player_interacted_with_entity"
        )
        return Advancement(
            {
                "criteria": {
                    "requirement": {
                        "trigger": f"minecraft:{criteria}",
                        "conditions": {
                            "entity": {
                                "type": "minecraft:interaction",
                                "nbt": f"{{Tags:['{interaction.tag_name}']}}",
                            }
                        },
                    }
                },
                "rewards": {"function": f"nbs:interaction/{function}"},
            }
        )

    if not (interaction.function_left or interaction.function_right):
        function_left = function_right = interaction.id
    else:
        function_left = interaction.function_left
        function_right = interaction.function_right

    if function_left:
        ctx.data[f"nbs:{interaction.id}_left"] = get_advancement("left", function_left)
        function_file = ctx.data.functions[f"nbs:interaction/{function_left}"]
        function_file.append(f"advancement revoke @s only nbs:{interaction.id}_left")
    if function_right:
        ctx.data[f"nbs:{interaction.id}_right"] = get_advancement(
            "right", function_right
        )
        function_file = ctx.data.functions[f"nbs:interaction/{function_right}"]
        function_file.append(f"advancement revoke @s only nbs:{interaction.id}_right")


def beet_default(ctx: Context):
    for interaction in interactions:
        generate_advancement(ctx, interaction)
