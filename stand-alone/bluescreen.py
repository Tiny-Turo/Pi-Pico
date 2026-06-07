import board, busio, displayio, terminalio
from fourwire import FourWire
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

displayio.release_displays()

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

display_bus = FourWire(
    spi,
    command=board.GP16,
    chip_select=board.GP17,
    reset=board.GP20
)

display = ST7735R(
    display_bus,
    width=128,
    height=160,
    bgr=True,
    colstart=0,
    rowstart=0,
)

splash = displayio.Group()
display.root_group = splash

bg = Rect(0, 0, 128, 160, fill=0x0000FF)  # black
splash.append(bg)

while True:
    pass