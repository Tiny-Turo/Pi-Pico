# fswatch -o src | xargs -n1 -I{} rsync -a --inplace --no-perms --no-owner --no-group \
#   --exclude '__pycache__' \
#   src/ /Volumes/CIRCUITPY/


import time
import screen as screen 
import players as players
import rotary_encoder as rotary_encoder

has_started = False

def press():
    global has_started

    if not has_started:
        players.spawn(screen.group)
        print(players.players_amount)
        has_started = True
    else:
        players.players[players.current_player].submit(screen.group)

def rotate(dir):
    if not has_started:
        players.players_amount += dir
        if players.players_amount <= 2: players.players_amount = 2
        print(players.players_amount)
    else:
        players.players[players.current_player].rotate(dir)

def load():
    print("Hello World!")

load()

while True:
    rotary_encoder.update(press, rotate)
    if has_started:
        players.update(screen.group)
    time.sleep(0.01)