# This file was generated by Animated Java via MC-Build. It is not recommended to edit this file directly.
scoreboard objectives add aj.animation_speaker_playing_120.frame dummy
scoreboard objectives add aj.animation_speaker_beat_1.frame dummy
scoreboard objectives add aj.animation_speaker_beat_2.frame dummy
scoreboard objectives add aj.animation_speaker_beat_3.frame dummy
scoreboard objectives add aj.animation_speaker_beat_4.frame dummy
execute as @e[type=item_display,tag=aj.music_speaker.root] unless score @s aj.is_rig_loaded matches 1 at @s run function animated_java:music_speaker/root/on_load