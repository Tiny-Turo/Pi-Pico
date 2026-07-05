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
MOVE_BY = 50

STEP = math.pi / 48

MIN_DISCOVER_WIDTH = 10
MAX_DISCOVER_WIDTH = math.pi * 5/8

DISCOVERY_AREA = 700


PLAYER_COLORS = [0x2D98BB,0xCFAF3C,0xD83E3E,0x883ED8,0x6BAB4B]

class Sector:
  def __init__(self, x, y, start_angle, end_angle, color, group):
    self.x = x
    self.y = y
    self.start_angle = min(start_angle, end_angle)
    self.end_angle = max(start_angle, end_angle)

    self.radius = self.calculate_radius_of_sector(abs(self.end_angle - self.start_angle))

    self.color = color

    self.add_sector_polygon(group)

  def add_sector_polygon(self, group):
    steps = 60
    sweep = abs(self.end_angle - self.start_angle)

    d = sweep / steps
    points = [(int(self.x), int(self.y))]  # center
    for i in range(steps + 1):
        a = self.start_angle + i * d
        px = int(self.x + self.radius * math.cos(a))
        py = int(self.y + self.radius * math.sin(a))
        points.append((px, py))
    # back to center to close shape
    points.append((int(self.x), int(self.y)))

    self.polygon = FilledPolygon(points=points, fill=self.color, outline=self.color)
    group.append(self.polygon)



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
    self.angle = 0

    self.area = []
    self.color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

    self.circle = Circle(0, 0, PLAYER_RADIUS, fill=self.color)
    self.circle.x = int(self.x)
    self.circle.y = int(self.y)

    self.line = Line(int(self.x) + PLAYER_RADIUS, int(self.y) + PLAYER_RADIUS, int(self.x + PLAYER_RADIUS + MOVE_BY * math.cos(self.angle)), int(self.y + PLAYER_RADIUS + MOVE_BY * math.sin(self.angle)), color=0x000000);
    self.sector = None

    self.discover_start = None
    self.discover_end = None

    group.append(self.circle)
    group.append(self.line)

  def update_line(self, group):
    group.remove(self.line)
    self.line = Line(int(self.x + PLAYER_RADIUS), int(self.y + PLAYER_RADIUS), int(self.x  + PLAYER_RADIUS + MOVE_BY * math.cos(self.angle)), int(self.y + PLAYER_RADIUS + MOVE_BY * math.sin(self.angle)), color=0x000000);
    group.append(self.line)
  
  def rotate(self, add, group):
      self.angle += add * STEP
      self.update_line(group)

      if current_stage == "Discover":
        if (not self.discover_start == None) and (self.discover_end == None):
          if abs(self.discover_start - self.angle) >= MAX_DISCOVER_WIDTH:
            if self.discover_start < self.angle: self.angle = self.discover_start + MAX_DISCOVER_WIDTH
            if self.discover_start > self.angle: self.angle = self.discover_start - MAX_DISCOVER_WIDTH

          if not abs(self.discover_start - self.angle) < STEP:
            if self.sector:
              group.remove(self.sector.polygon)
            self.sector = Sector(self.x + PLAYER_RADIUS, self.y + PLAYER_RADIUS, self.discover_start, self.angle, self.color, group)

  def submit(self, group):
    global current_stage, current_player

    if current_stage == "Discover":
      if self.discover_start == None:
        # Set the discover start
        self.discover_start = self.angle
        print("Discover Start: "+ str(self.discover_start))
      elif abs(self.discover_start - self.angle) > STEP: 
        self.discover_end = self.angle
        print("Discover End: "+ str(self.discover_end))
        print("Discover Start: "+ str(self.discover_start))

        sector = Sector(self.x + PLAYER_RADIUS, self.y + PLAYER_RADIUS, self.discover_start, self.discover_end, self.color, group)
        self.area.append(sector)

        # Check if you've hit any players
        for player in players:
          if player.index != self.index:
            if sector.is_colliding(player):
              print("GOOD JOB: COLLISION")

        # Reset variables
        self.discover_start = None
        self.discover_end = None

        current_stage = "Move"
    elif current_stage == "Move":
      # Update the acctual player
      self.x += MOVE_BY * math.cos(self.angle)
      self.y += MOVE_BY * math.sin(self.angle)

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

      self.circle.x = 1000
      self.line.x = 1000

      current_stage = "Change"
    elif current_stage == "Change":
      current_player += 1
      current_player = current_player % len(players)

      # Hide all other players by placing them off the screen
      for player in players:
        if player.index != current_player:
          player.circle.x = 1000
          player.line.x = 1000
        else:
          player.circle.x = int(player.x)
          player.line.x = int(player.x + PLAYER_RADIUS / 2)

      current_stage = "Discover"
    self.update_line(group)

def load(group):
  print("hi")

def update(group):
  global players
  current = players[current_player]


def spawn(group):
  for i in range(0, players_amount):
    players.append(Player(i, group))
