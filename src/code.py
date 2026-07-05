# fswatch -o src | xargs -n1 -I{} rsync -a --inplace --no-perms --no-owner --no-group \
#   --exclude '__pycache__' \
#   src/ /Volumes/CIRCUITPY/


import time
import screen as screen 
import players as players
import rotary_encoder as rotary_encoder

has_started = False

def press():
    if not has_started:
        players.spawn(screen.group)
    else:
        players.players[players.current_player].submit()
    print("pressed")

def rotate(dir):
    if not has_started:
        players.players_amount += 1
        if players.players_amount <= 2: players.players_amount = 2
    else:
        players.players[players.current_player].rotate()

def load():
    print("Hello World!")

load()

while True:
    rotary_encoder.update(press, rotate)
    if has_started:
        players.update()
    time.sleep(0.01)