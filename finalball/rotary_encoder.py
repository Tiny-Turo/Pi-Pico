import board
import digitalio
import time

# Setup encoder pins
clk = digitalio.DigitalInOut(board.GP2)
clk.direction = digitalio.Direction.INPUT
clk.pull = digitalio.Pull.UP

dt = digitalio.DigitalInOut(board.GP3)
dt.direction = digitalio.Direction.INPUT
dt.pull = digitalio.Pull.UP

# Optional switch
sw = digitalio.DigitalInOut(board.GP4)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

# Track last state
last_clk = clk.value
speed = 1

def update_rotary_encoder(reset):
    global last_clk, speed, clk, dt, sw
    current_clk = clk.value
    # Detect rising edge on CLK
    if last_clk == 0 and current_clk == 1:
        if dt.value != current_clk:
            speed *= 1.2  # Clockwise
        else:
            speed *= 0.9  # Counter-clockwise
        print("Position:", speed)
    
    # Optional: detect button press
    if not sw.value:
        speed = 1;
        reset()
        print("Button pressed!")
        time.sleep(0.2)  # debounce delay

    last_clk = current_clk

def get_speed():
    global speed
    return speed