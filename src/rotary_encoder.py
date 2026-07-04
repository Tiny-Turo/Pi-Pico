import board
import rotaryio
import digitalio

encoder = rotaryio.IncrementalEncoder(
    board.GP2,
    board.GP3
)

button = digitalio.DigitalInOut(board.GP4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

last_position = encoder.position
last_button = button.value

def update(press, turn):
    global last_position, last_button

    pos = encoder.position

    if pos != last_position:
        turn(pos - last_position)
        last_position = pos

    if last_button and not button.value:
        press()

    last_button = button.value