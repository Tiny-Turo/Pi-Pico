import random, math
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect



player = None

class Player:
  def __init__(self, group):
    self.width = 20.0
    self.height = 15.0
  
    x = 64 - self.width/2
    y = 160 - self.height

    group.append(Rect(0, int(y), 128, int(self.height), fill=0x4D5061))

    self.x = x
    self.y = y
    self.vx = 0
    self.triangle = Triangle(int(x), int(y), int(x + self.width/2), int(y + self.height), int(x - self.width/2), int(y + self.height), fill=0xE8C547)
    group.append(self.triangle)



def load(group):
  global player
  Ball(group, 0, 0, 1)
  Ball(group, 100, 0, 1)
  Ball(group, 50, 0, 1)

  player = Player(group)

def update():
  global player

  player.triangle.x = int(player.x)

def update_position(add):
  global player

  player.x += add * 6
  if player.x < 0: player.x = 0
  if player.x > 128 - player.width: player.x = 128 - player.width


def shoot_ball(group):
  Ball(group, player.x, player.y, 1, 0, -0.2)

def resolve_collision(a, b):
    # compute center positions
    ax = a.x + a.r
    ay = a.y + a.r
    bx = b.x + b.r
    by = b.y + b.r

    x_dist = bx - ax
    y_dist = by - ay
    dist = math.sqrt(x_dist * x_dist + y_dist * y_dist)
    if dist > a.r + b.r:
        return None

    if a.r == b.r:
        size_index = ball_sizes.index(b.r) + 1
        sx = (bx + ax) / 2
        sy = (by + ay) / 2
        return ("merge", a, b, sx, sy, size_index)

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
    overlap = (a.r + b.r) - dist
    if overlap > 0:
        sep = overlap / 2 + 1e-6
        ax -= nx * sep
        ay -= ny * sep
        bx += nx * sep
        by += ny * sep
        a.x = ax - a.r
        a.y = ay - a.r
        b.x = bx - b.r
        b.y = by - b.r

    return None

balls = []
ball_sizes = [5, 8, 12, 16, 20, 25]
ball_colors =  [0xE391D7, 0xE086D3, 0xE886B3, 0xF08693, 0xF88673,  0xFF8552]

class Ball:
  def __init__(self, group, x, y, size_index, vx = random.random() * 0.1 + 0.2, vy = random.random() * 0.1 + 0.2):
    if size_index > len(ball_sizes): return
    r = ball_sizes[size_index]

    self.x = x
    self.y = y

    self.vx = vx
    self.vy = vy
    
    self.r = r
    self.circle = Circle(int(self.x), int(self.y), r, fill=ball_colors[size_index % len(ball_colors)])
    group.append(self.circle)
    balls.append(self)

  def update(self, balls_list, group):
    self.x += self.vx
    self.y += self.vy

    self.collide(balls_list, group)

    if self.x < 0:
        self.x = 0
        self.vx *= -1
    if self.x + self.r * 2 > 128:
        self.x = 128 - self.r * 2
        self.vx *= -1
    if self.y < 0:
        self.y = 0
        self.vy *= -1
    if self.y + self.r * 2 > player.y:
        self.y = player.y - self.r * 2
        self.vy *= -1


    self.circle.x = int(self.x)
    self.circle.y = int(self.y)

  def collide(self, balls_list, group):
    for ball in list(balls_list):
      if ball is self:
        continue
      result = resolve_collision(self, ball)
      if result is None:
        continue
      if result[0] == "merge":
        _, a_obj, b_obj, sx, sy, size_index = result
        # remove both objects (if still present)
        for obj in (a_obj, b_obj):
          if obj in balls_list:
            try:
              group.remove(obj.circle)
            except ValueError:
              pass
            balls_list.remove(obj)
        # create new larger ball (cap size_index to max)
        size_index = min(size_index, len(ball_sizes) - 1)
        Ball(group, sx - ball_sizes[size_index], sy - ball_sizes[size_index], size_index)
        return


def update_balls(group):
  for ball in list(balls):
    if ball is None:
       continue
    ball.update(balls, group)
  for ball in balls:

     if ball is None: 
        balls.remove(ball)
        group.remove(ball.circle)