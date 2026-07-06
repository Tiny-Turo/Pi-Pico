# fswatch -o src | xargs -n1 -I{} rsync -a --inplace --no-perms --no-owner --no-group \
#   --exclude '__pycache__' \
#   src/ /Volumes/CIRCUITPY/


import time
import screen as screen 
import players as players
import rotary_encoder as rotary_encoder
from adafruit_display_text.label import Label
import terminalio

has_started = False
players_amount_text = None
text = None


def press():
    global has_started

    if not has_started:
        players.spawn(screen.group)
        print("Players: " + str(players.players_amount))
        has_started = True
        screen.group.remove(text)
        screen.group.remove(players_amount_text)
        players.first_round(screen.group)
    else:
        players.players[players.current_player].submit(screen.group)

def rotate(dir):
    if not has_started:
        players.players_amount += dir
        if players.players_amount <= 2: players.players_amount = 2
        players_amount_text.text = "Players: " + str(players.players_amount)
    else:
        players.players[players.current_player].rotate(dir, screen.group)

def load():
    global players_amount_text, text
    text = Label(
        terminalio.FONT,
        text="Hello World!",
        color=0xFFFFFF,
        x=10,
        y=20
    )
    players_amount_text = Label(
        terminalio.FONT,
        text="Players: 2",
        color=0xFFFFFF,
        x=20,
        y=40
    )
    screen.group.append(text)
    screen.group.append(players_amount_text)

    print("Hello World!")

load()

while True:
    rotary_encoder.update(press, rotate)
    if has_started:
        players.update(screen.group)
    time.sleep(0.01)