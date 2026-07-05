import random, math
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect

players_amount = 2
current_player = 0
current_stage = "Discover" #  Discover, Move Change

# List of all players
players = []

# Variables which are the same for every player
PLAYER_RADIUS = 10
MOVE_BY = 30

MIN_DISCOVER_WIDTH = 10
MAX_DISCOVER_WIDTH = math.pi

DISCOVERY_AREA = 10


PLAYER_COLORS = [0xCFAF3C,0x2D98BB,0xD83E3E,0x883ED8,0x6BAB4B]

class Sector:
  def __init__(self, x, y, startAngle, endAngle):
    self.radius = self.calculate_radius_of_sector(abs(startAngle - endAngle))

    self.x = x
    self.y = y
    self.startAngle = startAngle
    self.endAngle = endAngle


  def calculate_radius_of_sector(angle):
    radius = math.pow((2 * DISCOVERY_AREA) / angle, 1/2)
    return radius

class Player:
  def __init__(self, i, group):
    self.x = 100
    self.y = 100
    self.area = []
    self.color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

    self.circle = Circle(int(self.x), int(self.y), PLAYER_RADIUS, fill=self.color)
    self.angle = 0

    self.discoverStart = None
    self.discoverEnd = None


    group.append(self.circle)
  
  def rotate(self, add):
      self.angle += add * math.pi/12

  def submit(self):
    if current_stage == "Discover":
      if not self.discoverStart:
        # Set the discover start
        self.discoverStart = self.angle
      else: 
        self.discoverEnd = self.angle

        # SUBMIT FIRST, then reset all the variables to ready for next round
        self.area.append(Sector(self.x, self.y, self.discoverStart, self.discoverEnd))
        self.discoverStart = None
        self.angle = 0
        self.discoverWidth = 0

        current_stage = "Move"
    elif current_stage == "Move":
      # Update the acctual player
      self.x += MOVE_BY * math.sin(self.angle)
      self.y += MOVE_BY * math.sin(self.angle)

      # Update the sprite
      self.circle.x = int(self.x)
      self.circle.y = int(self.y)

      # Reset the angle
      self.angle = 0
      current_stage = "Change"

    elif current_stage == "Change":
      current_player += 1

      current_stage = "Discover"
      
def load(group):

def update():
  
def spawn(group):
  for i in range(0, players_amount):
    players.append(Player(i, group))