#!tag "minecraft:tick"

#!set note_function = generate_path("note")

execute if score songindex nbs matches {{ song_index }} run function {{ note_function }}

#!function note_function
    #!for node in generate_song()
        #!function node.parent append
            #!if node.partition(8)
                execute if score songtime nbs matches {{ node.range }} run function {{ node.children }}
            #!else
                #!set notes = node.value[1]

                #!if notes | length == 1
                    execute if score songtime nbs matches {{ node.range }} as @e[tag=nbs_speaker] at @s run {{ notes[0].play("@a[distance=..128]", song_source) }}
                #!else
                    #!set chord_function = generate_path("chord/{hash}", notes)
                    execute if score songtime nbs matches {{ node.range }} as @e[tag=nbs_speaker] at @s run function {{ chord_function }}

                    #!function chord_function
                        #!for note in notes
                            {{ note.play("@a[distance=..128]", song_source) }}
                        #!endfor
                    #!endfunction
                #!endif
            #!endif
        #!endfunction
    #!endfor
#!endfunction
