import board, busio, displayio
import time
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

colorIndex = 0
colors = [0xFF0000, 0xFFFF00, 0x00FF00, 0x00FFFF, 0x0000FF,  0xFF00FF]

# rect
RECT_SIZE = 40

rect = Rect(10, 10, 40, 40, fill=colors[colorIndex])
group.append(rect)

# Position + speed
x = 10.0
y = 10.0
vx = 3.2
vy = 3.2


while True:
    x += vx
    y += vy

    # Bounce off walls
    if x <= 0 or x >= 128 - RECT_SIZE:
        vx *= -1
        colorIndex += 1
    if y <= 0 or y >= 160 - RECT_SIZE:
        vy *= -1
        colorIndex += 1

    colorIndex = colorIndex % len(colors)

    # Move rect
    rect.x = int(x)
    rect.y = int(y)

    rect.fill = colors[colorIndex]

    time.sleep(0.02)