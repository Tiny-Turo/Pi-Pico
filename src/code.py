import time
import src.screen as screen 
import src.player as player
import src.rotary_encoder as rotary_encoder

def press():
    player.shoot_ball(screen.group)

def turn(dir):
    player.update_position(dir)

def load():
    player.load(screen.group)

load()

while True:
    player.update()
    player.update_balls(screen.group)
    rotary_encoder.update(press, turn)
    time.sleep(0.01)

