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
position = 1

last_press_time = 0

def update(press, turn):
    global last_clk, position, clk, dt, sw, last_press_time
    current_clk = clk.value
    # Detect rising edge on CLK
    if last_clk == 0 and current_clk == 1:
        if dt.value != current_clk:
            turn(1)
            position += 1  # Clockwise
        else:
            turn(-1)
            position -= 1  # Counter-clockwise
        print("Position:", position)
    
    # Optional: detect button press
    if not sw.value:
        if time.time() - last_press_time > 0.2:
            last_press_time = time.time()
            press()
            print("Button pressed!")

    last_clk = current_clk

