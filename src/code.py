# fswatch -o src | xargs -n1 -I{} rsync -a --inplace --no-perms --no-owner --no-group \
#   --exclude '__pycache__' \
#   src/ /Volumes/CIRCUITPY/


import time
import screen as screen 
import player as player
import rotary_encoder as rotary_encoder

def press():
    print("hi")

def turn(dir):
    player.update_position(dir)

def load():
    player.load(screen.group)

load()

while True:
    player.update()
    rotary_encoder.update(press, turn)
    time.sleep(0.01)