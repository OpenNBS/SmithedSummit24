scoreboard players set songtime nbs -1
scoreboard players remove songindex nbs 1
execute if score songindex nbs matches ..-1 run scoreboard players set songindex nbs 10