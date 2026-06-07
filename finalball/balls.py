import time, random, math

import board, busio, displayio
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


MAX_W = 128
MAX_H = 160
GROW_BY = 1
balls = []

colors = [0xFF0000, 0xFFFF00, 0x00FF00, 0x00FFFF, 0x0000FF,  0xFF00FF]
def load_balls():   
    global balls
    balls = []
    for i in range(6):
        r = 10
        # X and Y are top-left; keep fully inside bounds
        x = random.random() * (MAX_W - 2 * r)
        y = random.random() * (MAX_H - 2 * r)
        ball = Circle(int(x), int(y), int(r), fill=colors[i % len(colors)])
        ball._r = r
        ball._x = float(x)   # top-left x (float for smooth movement)
        ball._y = float(y)   # top-left y
        ball.vx = random.random() * 0.3 + 0.2
        ball.vy = random.random() * 0.3 + 0.2
        balls.append(ball)

        if i < len(group):
            group[i] = ball
        else:
            group.append(ball)    

   


def resolve_collision(a, b, ia, ib):
    # compute center positions from top-left coords
    ax = a._x + a._r
    ay = a._y + a._r
    bx = b._x + b._r
    by = b._y + b._r

    x_dist = bx - ax
    y_dist = by - ay
    dist = math.sqrt(x_dist * x_dist + y_dist * y_dist)
    if dist > a._r + b._r:
        return

    if dist == 0:
        nx, ny = 1.0, 0.0
    else:
        nx, ny = x_dist / dist, y_dist / dist

    # relative velocity
    rvx = b.vx - a.vx
    rvy = b.vy - a.vy

    # velocity along normal
    vel_norm = rvx * nx + rvy * ny
    if vel_norm >= 0:
        return  # already separating

    # equal-mass elastic: swap normal components
    a_nv = a.vx * nx + a.vy * ny
    b_nv = b.vx * nx + b.vy * ny
    new_a_nv = b_nv
    new_b_nv = a_nv

    # tangent components unchanged
    tx, ty = -ny, nx
    a_tv = a.vx * tx + a.vy * ty
    b_tv = b.vx * tx + b.vy * ty

    # reconstruct velocities
    a.vx = new_a_nv * nx + a_tv * tx
    a.vy = new_a_nv * ny + a_tv * ty
    b.vx = new_b_nv * nx + b_tv * tx
    b.vy = new_b_nv * ny + b_tv * ty

    # positional correction: operate in center-space then convert back to top-left
    overlap = (a._r + b._r) - dist
    if overlap > 0:
        sep = overlap / 2 + 1e-6
        ax -= nx * sep
        ay -= ny * sep
        bx += nx * sep
        by += ny * sep
        a._x = ax - a._r
        a._y = ay - a._r
        b._x = bx - b._r
        b._y = by - b._r

    # shrink both a bit on collision (indices passed in)
    replace_ball(ia, -GROW_BY * 2)
    replace_ball(ib, -GROW_BY * 2)

def update_balls(speed):
  for i, ball in enumerate(balls):
      if ball == None: continue

      ball._x += ball.vx * speed 
      ball._y += ball.vy * speed 

      # Bounce off walls
      if ball._x <= 0 or ball._x >= MAX_W - ball._r * 2:
          ball.vx *= -1
          replace_ball(i, GROW_BY)
      if ball._y <= 0 or ball._y >= MAX_H - ball._r * 2:
          ball.vy *= -1
          replace_ball(i, GROW_BY)

      for j, ball_2 in enumerate(balls):
        if ball == None or ball_2 == None: continue
        if j == i: continue
        resolve_collision(ball_2, ball, j, i)

      if ball == None: continue
      ball.x = int(ball._x)
      ball.y = int(ball._y)


def replace_ball(i, grow):
    if i < 0 or i >= len(balls):
        return
    
    if not balls[i]:
        return
    
    old = balls[i]
    new_r = int(old._r + grow)
    if new_r < 1:
        try:
            group.remove(old)
        except ValueError:
            pass
        balls[i] = None
        return

    # create new Circle using top-left integer coords
    new_ball = Circle(int(old._x), int(old._y), int(new_r), fill=old.fill)
    new_ball.vx = old.vx
    new_ball.vy = old.vy
    new_ball._r = new_r
    new_ball._x = old._x
    new_ball._y = old._y

    balls[i] = new_ball
    try:
        group.remove(old)
    except ValueError:
        pass
    group.append(new_ball)

    # clamp top-left to bounds
    if new_ball._x < 0:
        new_ball._x = 0
    if new_ball._x + new_ball._r * 2 > MAX_W:
        new_ball._x = MAX_W - new_ball._r * 2
    if new_ball._y < 0:
        new_ball._y = 0
    if new_ball._y + new_ball._r * 2 > MAX_H:
        new_ball._y = MAX_H - new_ball._r * 2

    new_ball.x = int(new_ball._x)
    new_ball.y = int(new_ball._y)
