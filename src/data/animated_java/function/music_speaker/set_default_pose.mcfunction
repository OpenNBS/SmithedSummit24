# This file was generated by Animated Java via MC-Build. It is not recommended to edit this file directly.
execute unless entity @s[type=item_display,tag=aj.music_speaker.root] run return run function animated_java:global/errors/function_not_executed_as_root_entity {'export_namespace': 'music_speaker', 'function_path': 'animated_java:music_speaker/set_default_pose'}
execute on passengers if entity @s[tag=aj.music_speaker.bone.antenna] run data merge entity @s {transformation: [-1f,0f,1.2246467991473532e-16f,-0.625f,0f,1f,0f,0.75f,-1.2246467991473532e-16f,0f,-1f,-0.18750000000000008f,0f,0f,0f,1f], start_interpolation: -1}
execute on passengers if entity @s[tag=aj.music_speaker.bone.speaker_1] run data merge entity @s {transformation: [-1f,0f,1.2246467991473532e-16f,-0.46875000000000006f,0f,1f,0f,0.28125f,-1.2246467991473532e-16f,0f,-1f,0.24999999999999994f,0f,0f,0f,1f], start_interpolation: -1}
execute on passengers if entity @s[tag=aj.music_speaker.bone.speaker_2] run data merge entity @s {transformation: [-1f,0f,1.2246467991473532e-16f,0.46874999999999994f,0f,1f,0f,0.28125f,-1.2246467991473532e-16f,0f,-1f,0.25000000000000006f,0f,0f,0f,1f], start_interpolation: -1}
execute on passengers if entity @s[tag=aj.music_speaker.bone.text_display] run data merge entity @s {transformation: [0.2f,0f,-4.898587196589413e-17f,-0.006250000000000026f,0f,0.2f,0f,0.571875f,4.898587196589413e-17f,0f,0.2f,0.2515625f,0f,0f,0f,1f], start_interpolation: -1}
execute on passengers if entity @s[tag=aj.music_speaker.bone.details] run data merge entity @s {transformation: [-1f,0f,1.2246467991473532e-16f,0.04687499999999998f,0f,1f,0f,0.390625f,-1.2246467991473532e-16f,0f,-1f,0.1953125f,0f,0f,0f,1f], start_interpolation: -1}
execute on passengers if entity @s[tag=aj.music_speaker.bone.stereo] run data merge entity @s {transformation: [-1f,0f,1.2246467991473532e-16f,0f,0f,1f,0f,0.375f,-1.2246467991473532e-16f,0f,-1f,0f,0f,0f,0f,1f], start_interpolation: -1}