import board, busio, displayio
import time, random
from fourwire import FourWire
from adafruit_st7735r import ST7735R
from adafruit_display_shapes.circle import Circle

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

# rect
BALL_SIZE = 2
balls = []

for i in range(1, 40):
  ball = Circle(10, 10, BALL_SIZE, fill=0xFF0000)
  ball._x = 10
  ball._y = 10
  ball.vx = random.random() * 3 + 2
  ball.vy = random.random() * 3 + 2
  balls.append(ball)
  group.append(ball)

while True:
    for ball in balls:

      ball._x += ball.vx
      ball._y += ball.vy

      # Bounce off walls
      if ball._x <= 0 or ball._x >= 128 - BALL_SIZE*2:
          ball.vx *= -1
      if ball._y <= 0 or ball._y >= 160 - BALL_SIZE*2:
          ball.vy *= -1


      ball.x = int(ball._x)
      ball.y = int(ball._y)


    time.sleep(0.02)