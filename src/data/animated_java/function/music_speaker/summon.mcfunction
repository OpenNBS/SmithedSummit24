# This file was generated by Animated Java via MC-Build. It is not recommended to edit this file directly.
data modify storage aj:temp args set value {variant:'', animation:'', frame: 0}
$execute store success score #success aj.i run data modify storage aj:temp args set value $(args)
summon minecraft:item_display ~ ~ ~ { Tags:['aj.new','aj.rig_entity','aj.rig_root','aj.music_speaker.root','nbs_speaker'], teleport_duration: 0, interpolation_duration: 1, Passengers:[{id:"minecraft:marker",Tags:["aj.rig_entity","aj.data","aj.music_speaker.data"],data:{rigHash:"161acab26de4cba90bedfd171f5231a5a315b02ec9aef87b4b4f73d03abc5813",locators:{},cameras:{},bones:{data_data:"",bone_antenna:"",bone_speaker_1:"",bone_speaker_2:"",text_display_text_display:"",bone_details:"",bone_stereo:""}}},{Tags:["aj.rig_entity","aj.bone","aj.music_speaker.bone","aj.music_speaker.bone.antenna"],id:"minecraft:item_display",transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},interpolation_duration:1,teleport_duration:0,item_display:"head",item:{id:"minecraft:white_dye",count:1,components:{"minecraft:custom_model_data":18483}},height:48f,width:48f},{Tags:["aj.rig_entity","aj.bone","aj.music_speaker.bone","aj.music_speaker.bone.speaker_1"],id:"minecraft:item_display",transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},interpolation_duration:1,teleport_duration:0,item_display:"head",item:{id:"minecraft:white_dye",count:1,components:{"minecraft:custom_model_data":18484}},height:48f,width:48f},{Tags:["aj.rig_entity","aj.bone","aj.music_speaker.bone","aj.music_speaker.bone.speaker_2"],id:"minecraft:item_display",transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},interpolation_duration:1,teleport_duration:0,item_display:"head",item:{id:"minecraft:white_dye",count:1,components:{"minecraft:custom_model_data":18485}},height:48f,width:48f},{Tags:["aj.rig_entity","aj.bone","aj.music_speaker.bone","aj.music_speaker.bone.text_display"],id:"minecraft:text_display",transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},interpolation_duration:1,teleport_duration:0,height:48f,width:48f,text:"\"Now Playing:\"",background:0,line_width:150,shadow:0b,see_through:0b},{Tags:["aj.rig_entity","aj.bone","aj.music_speaker.bone","aj.music_speaker.bone.details"],id:"minecraft:item_display",transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},interpolation_duration:1,teleport_duration:0,item_display:"head",item:{id:"minecraft:white_dye",count:1,components:{"minecraft:custom_model_data":18486}},brightness:{block:15f,sky:15f},height:48f,width:48f},{Tags:["aj.rig_entity","aj.bone","aj.music_speaker.bone","aj.music_speaker.bone.stereo"],id:"minecraft:item_display",transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},interpolation_duration:1,teleport_duration:0,item_display:"head",item:{id:"minecraft:white_dye",count:1,components:{"minecraft:custom_model_data":18482}},height:48f,width:48f}], }
execute as @e[type=item_display,tag=aj.new,limit=1,distance=..0.01] run function animated_java:music_speaker/zzz/0