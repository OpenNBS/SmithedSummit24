import json
from dataclasses import dataclass

from beet import Advancement, Context, Function

painting_tellraw = 'tellraw @s ["","\\n",{"text":"========================================","bold":true,"strikethrough":true,"color":"dark_purple"},"\\n","\\n",{"text":"  <author> >>","bold":true,"color":"light_purple"},"\\n","\\n",{"text":"   Songs:","color":"yellow"},<songs>"\\n","\\n",{"text":"   ⛏ ","color":"white"},{"text":"<minecraft>","color":"dark_green","hoverEvent":{"action":"show_text","contents":["Minecraft username"]}},"\\n",{"text":"   🎮 ","color":"white"},{"text":"@<discord>","color":"#5865F2","hoverEvent":{"action":"show_text","contents":[{"text":"Discord username","color":"white"}]}},"\\n",{"text":"   📺 ","color":"white"},{"text":"<youtube>","underlined":true,"color":"#FF0000","clickEvent":{"action":"open_url","value":"https://youtube.com/<youtube>"},"hoverEvent":{"action":"show_text","contents":[{"text":"https://youtube.com/<youtube>","color":"yellow"}]}},"\\n","\\n",{"text":"========================================","bold":true,"strikethrough":true,"color":"dark_purple"}]'

song_tellraw = (
    '"\\n",{"text":"     -  ","color":"gray"},{"text":"<song>","color":"white"},'
)


@dataclass
class Interaction:
    id: str
    tag_name: str
    function_left: Function | None = None
    function_right: Function | None = None


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
                "rewards": {"function": function},
            }
        )

    if interaction.function_left is interaction.function_right:
        function_left = function_right = f"nbs:interaction/{interaction.id}"
    else:
        function_left = f"nbs:interaction/{interaction.id}_left"
        function_right = f"nbs:interaction/{interaction.id}_right"

    if function_left:
        advancement_id = f"nbs:{interaction.id}_left"
        ctx.data[advancement_id] = get_advancement("left", function_left)
        if interaction.function_left:
            ctx.data[function_left] = interaction.function_left
        ctx.data.functions[function_left].append(
            f"advancement revoke @s only {advancement_id}"
        )
    if function_right:
        advancement_id = f"nbs:{interaction.id}_right"
        ctx.data[advancement_id] = get_advancement("right", function_right)
        if interaction.function_right:
            ctx.data[function_right] = interaction.function_right
        ctx.data.functions[function_right].append(
            f"advancement revoke @s only {advancement_id}"
        )


def beet_default(ctx: Context):

    with open(ctx.directory / "src" / "authors.json", "r") as f:
        authors = json.load(f)

    for author_data in authors:
        author_id = author_data["author"].lower().replace(" ", "_")

        songs_str = "".join(
            song_tellraw.replace("<song>", song) for song in author_data["songs"]
        )
        tellraw = (
            painting_tellraw.replace("<author>", author_data["author"])
            .replace("<songs>", songs_str)
            .replace("<minecraft>", author_data["minecraft"])
            .replace("<discord>", author_data["discord"])
            .replace("<youtube>", author_data["youtube"])
        )
        click_function = Function(
            [tellraw, "scoreboard players add paintings_clicked nbs_stats 1"]
        )
        interaction = Interaction(
            id=f"painting_{author_id}",
            tag_name=f"nbs_painting_{author_id}",
            function_left=click_function,
            function_right=click_function,
        )
        interactions.append(interaction)

    for interaction in interactions:
        generate_advancement(ctx, interaction)
