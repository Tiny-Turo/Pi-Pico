import random, math
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.arc import Arc
from adafruit_display_shapes.filled_polygon import FilledPolygon
from adafruit_display_shapes.line import Line

players_amount = 2
current_player = 0
current_stage = "Discover" #  Discover, Move Change

# List of all players
players = []

# Variables which are the same for every player
PLAYER_RADIUS = 10
MOVE_BY = 60

MIN_DISCOVER_WIDTH = 10
MAX_DISCOVER_WIDTH = math.pi

DISCOVERY_AREA = 300


PLAYER_COLORS = [0xCFAF3C,0x2D98BB,0xD83E3E,0x883ED8,0x6BAB4B]

class Sector:
  def __init__(self, x, y, start_angle, end_angle, color, group):
    self.radius = self.calculate_radius_of_sector(abs(start_angle - end_angle))

    self.x = x
    self.y = y
    self.start_angle = start_angle
    self.end_angle = end_angle

    self.color = color

    self.add_sector_polygon(group)

  def add_sector_polygon(self, group):
    steps = 60
    sweep = self.end_angle - self.start_angle
    if sweep < 0:
        sweep += 2 * math.pi

    d = sweep / steps
    points = [(int(self.x), int(self.y))]  # center
    for i in range(steps + 1):
        a = self.start_angle + i * d
        px = int(self.x + self.radius * math.cos(a))
        py = int(self.y + self.radius * math.sin(a))
        points.append((px, py))
    # back to center to close shape
    points.append((int(self.x), int(self.y)))

    polygon = FilledPolygon(points=points, fill=self.color, outline=self.color)
    group.append(polygon)



  def calculate_radius_of_sector(self, angle):
    radius = math.pow((2 * DISCOVERY_AREA) / angle, 1/2)
    return radius
  

  def is_colliding(self, player):
    # Calculate distance to player from centers
    dx = self.x - player.x
    dy = self.y - player.y
    distance = math.sqrt(dx * dx + dy * dy);

    # Calculate angle from center of sector to player center
    angle_to_player = (math.atan2(dy, dx) + math.pi * 2) % (math.pi * 2)

    # Calculate angle from center of sector to player edges
    dx1 = self.x - (player.x + math.cos(angle_to_player + math.pi / 2) * PLAYER_RADIUS)
    dy1 = self.y - (player.y + math.sin(angle_to_player + math.pi / 2) * PLAYER_RADIUS);
    ang1 = (math.atan2(dy1, dx1) + math.pi * 2) % (math.pi * 2);

    dx2 = self.x - (player.x + math.cos(angle_to_player - math.pi / 2) * PLAYER_RADIUS)
    dy2 = self.y - (player.y + math.sin(angle_to_player - math.pi / 2) * PLAYER_RADIUS);
    ang2 = (math.atan2(dy2, dx2) + math.pi * 2) % (math.pi * 2);

    is_angles_right = (ang1 < self.end_angle and ang1 > self.start_angle) or (ang2 < self.end_angle and ang2 > self.start_angle)
    has_collided = (is_angles_right and distance < PLAYER_RADIUS + self.radius) or distance < PLAYER_RADIUS

    return has_collided

class Player:
  def __init__(self, i, group):
    self.index = i

    self.x = random.uniform(0, 100)
    self.y = random.uniform(0, 100)
    self.angle =2

    self.area = []
    self.color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

    self.circle = Circle(int(self.x), int(self.y), PLAYER_RADIUS, fill=self.color)
    self.line = Line(int(self.x), int(self.y), int(self.x + MOVE_BY * math.sin(self.angle)), int(self.y + MOVE_BY * math.cos(self.angle)), color=self.color)
    self.line.stroke = 30


    self.discoverStart = None
    self.discoverEnd = None

    group.append(self.circle)
    group.append(self.line)

  
  def rotate(self, add):
      self.angle += add * math.pi/12
      print(self.angle)

  def submit(self, group):
    global current_stage, current_player

    print(current_stage)
    if current_stage == "Discover":
      if not self.discoverStart:
        # Set the discover start
        self.discoverStart = self.angle
      else: 
        self.discoverEnd = self.angle

        print(self.discoverStart - self.discoverEnd)
        # SUBMIT FIRST, then reset all the variables to ready for next round
        sector = Sector(self.x, self.y, self.discoverStart, self.discoverEnd, self.color, group)
        self.area.append(sector)

        # Check if you've hit any players
        for player in players:
          if player.index != self.index:
            if sector.is_colliding(player):
              print("GOOD JOB: COLLISION")

        # Reset variables
        self.discoverStart = None
        self.angle = 0
        self.discoverWidth = 0

        current_stage = "Move"
    elif current_stage == "Move":
      # Update the acctual player
      self.x += MOVE_BY * math.sin(self.angle)
      self.y += MOVE_BY * math.cos(self.angle)

      # Check if you've hit any areas 
      for player in players:
        if player.index != self.index:
          for sector in player.area:
            if sector.is_colliding(self):
              print("WHOOPS: HIT AN AREA")

      # Update the sprite
      self.circle.x = int(self.x)
      self.circle.y = int(self.y)

      # Reset the angle
      self.angle = 0
      current_stage = "Change"

    elif current_stage == "Change":
      current_player += 1
      current_player = current_player % len(players)

      # Hide all other players by placing them off the screen
      for player in players:
        if player.index != current_player:
          player.circle.x = 1000
        else:
          player.circle.x = int(player.x)

      current_stage = "Discover"

def load(group):
  print("hi")

def update():
  global players
  current = players[current_player]
  current.line.x = int(current.x + PLAYER_RADIUS / 2)
  current.line.y = int(current.y + PLAYER_RADIUS / 2)
  current.line.x1 = int(current.x + MOVE_BY * math.sin(current.angle)+ PLAYER_RADIUS / 2)
  current.line.y1 = int(current.y + MOVE_BY * math.cos(current.angle) + PLAYER_RADIUS / 2)
  
def spawn(group):
  for i in range(0, players_amount):
    players.append(Player(i, group))
