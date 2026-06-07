
import board, busio, displayio
from fourwire import FourWire
from adafruit_st7735r import ST7735R
from adafruit_display_shapes.rect import Rect

displayio.release_displays()

# SPI setup (standard Pico pins)
spi = busio.SPI(board.GP18, MOSI=board.GP19)

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
)

# Screen group
group = displayio.Group()
display.root_group = group

background = Rect(0, 0, 128, 160, fill=0x30323D) 
group.append(background)