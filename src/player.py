import random, math
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect

player = None

class Player:
  def __init__(self, group):
    self.width = 20.00
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

  player = Player(group)

def update():
  global player

  player.triangle.x = int(player.x)

def update_position(add):
  global player

  player.x += add * 6
  if player.x < 0: player.x = 0
  if player.x > 128 - player.width: player.x = 128 - player.width