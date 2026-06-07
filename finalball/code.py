import time, random
from balls import update_balls, load_balls
from rotary_encoder import get_speed, update_rotary_encoder

def reset():
    load_balls()


while True:
    update_rotary_encoder(reset)
    update_balls(get_speed())

    time.sleep(0.001)

