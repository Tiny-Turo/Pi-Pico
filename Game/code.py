import time
import screen 
import player
import rotary_encoder

def press():
    player.shoot_ball(screen.group)

def turn(dir):
    player.update_position(dir)

def load():
    player.load(screen.group)

load()

while True:
    rotary_encoder.update(press, turn)
    player.update()
    player.update_balls(screen.group)
    time.sleep(0.001)

