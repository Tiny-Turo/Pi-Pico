import board
import digitalio
import time

# Setup encoder pins
clk = digitalio.DigitalInOut(board.GP2) # pin 4
clk.direction = digitalio.Direction.INPUT
clk.pull = digitalio.Pull.UP

dt = digitalio.DigitalInOut(board.GP3) # pin 5
dt.direction = digitalio.Direction.INPUT
dt.pull = digitalio.Pull.UP

# Optional switch
sw = digitalio.DigitalInOut(board.GP4) # pin 6
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

# Track last state
last_clk = clk.value
position = 0

while True:
    current_clk = clk.value
    # Detect rising edge on CLK
    if last_clk == 0 and current_clk == 1:
        if dt.value != current_clk:
            position += 1  # Clockwise
        else:
            position -= 1  # Counter-clockwise
        print("Position:", position)
    
    # Optional: detect button press
    if not sw.value:
        print("Button pressed!")
        time.sleep(0.2)  # debounce delay

    last_clk = current_clk
    time.sleep(0.001)  # small delay