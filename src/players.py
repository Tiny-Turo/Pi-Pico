import random, math
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.filled_polygon import FilledPolygon
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect

import terminalio


players_amount = 2
current_player = 0
current_stage = "Discover" #  Discover, Move Change

change_player_text = None

# List of all players
players = []

# Variables which are the same for every player
PLAYER_RADIUS = 5
MOVE_BY = 24

STEP = math.pi / 24

MIN_DISCOVER_WIDTH = 10
MAX_DISCOVER_WIDTH = math.pi * 5/8

DISCOVERY_AREA = 350

PLAYER_COLORS = [0x2D98BB,0xCFAF3C,0xD83E3E,0x883ED8,0x6BAB4B]
AREA_COLORS = [0x3f7893,0xa18d40,0x9f3c37,0x6535a7,0x618846]
COLOR_NAME = ["Blue", "Yellow", "Red", "Purple", "Green"]

def lerp(a, b, t):
  return a + t * (b - a)

sector_draw_layer = 1
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
    global sector_draw_layer
    sweep = abs(self.end_angle - self.start_angle)
    steps = math.floor((sweep / STEP) * 2)

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
    group.insert(sector_draw_layer, self.polygon)
    sector_draw_layer += 1


  def calculate_radius_of_sector(self, angle):
    radius = math.pow((2 * DISCOVERY_AREA) / angle, 1/2)
    return radius
  
  def is_colliding(self, player, group):
    x1 = player.x + PLAYER_RADIUS
    y1 = player.y + PLAYER_RADIUS

    # DEBUG
    # group.append(Rect(
    #   x=int(x1),
    #   y=int(y1),
    #   width=5,
    #   height=5,
    #   fill=0xFF0000,
    # ))
    
    # Calculate distance to player from centers
    dx = x1 - self.x
    dy = y1 - self.y
    distance = math.sqrt(dx * dx + dy * dy);

    # Calculate angle from center of sector to player center
    angle_to_player = (math.atan2(dy, dx) + math.pi * 2) % (math.pi * 2)
    print("Angle To Player:" + str(angle_to_player))

    # Calculate angle from center of sector to player edges
    dx1 = (x1 + math.cos(angle_to_player + math.pi / 2) * PLAYER_RADIUS) - self.x
    dy1 = (y1 + math.sin(angle_to_player + math.pi / 2) * PLAYER_RADIUS) - self.y;
    ang1 = (math.atan2(dy1, dx1) + math.pi * 2) % (math.pi * 2);


    # DEBUG
    # group.append(Rect(
    #   x=int((x1 + math.cos(angle_to_player + math.pi / 2) * PLAYER_RADIUS)),
    #   y=int((y1 + math.sin(angle_to_player + math.pi / 2) * PLAYER_RADIUS)),
    #   width=5,
    #   height=5,
    #   fill=0x00FF00,
    # ))
    dx2 = (x1 + math.cos(angle_to_player - math.pi / 2) * PLAYER_RADIUS) - self.x
    dy2 = (y1 + math.sin(angle_to_player - math.pi / 2) * PLAYER_RADIUS) - self.y;
    ang2 = (math.atan2(dy2, dx2) + math.pi * 2) % (math.pi * 2);

    # DEBUG
    # group.append(Rect(
    #   x=int((x1 + math.cos(angle_to_player - math.pi / 2) * PLAYER_RADIUS)),
    #   y=int((y1 + math.sin(angle_to_player - math.pi / 2) * PLAYER_RADIUS)),
    #   width=5,
    #   height=5,
    #   fill=0x0000FF,
    # ))
    sweep = self.start_angle - self.end_angle
    while self.start_angle < 0:
      self.start_angle += math.pi * 2
    self.start_angle = self.start_angle % (math.pi * 2)
    self.end_angle = self.start_angle - sweep
    
    is_angles_right = False
    tests = 30
    for i in range(tests):
      a = lerp(ang1, ang2, i / (tests - 1))
      if self.start_angle <= a <= self.end_angle:
        is_angles_right = True
        break
   
    has_collided = (is_angles_right and distance < PLAYER_RADIUS + self.radius) or distance < PLAYER_RADIUS

    return has_collided

class Arrow:
  def __init__(self, x1, y1, x2, y2, color, width=1.5, head_width=9, head_length=6):
    self.width = width
    self.head_width = head_width
    self.head_length = head_length

    self.color = color

    self.points = self.calculate_points(x1, y1, x2, y2)

    self.polygon = FilledPolygon(
        points=self.points,
        outline=color,
        fill=color,
    )

  def calculate_points(self, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        return [(x1, y1)] * 7

    # Unit vectors
    ux = dx / length
    uy = dy / length

    # Perpendicular
    px = -uy
    py = ux

    shaft = self.width / 2
    head_width = self.head_width
    head_length = self.head_length

    # Base of the arrow head
    hx = x2 - ux * head_length
    hy = y2 - uy * head_length

    return [
        (int(x1 + px * shaft), int(y1 + py * shaft)),            # Back left
        (int(hx + px * shaft), int(hy + py * shaft)),            # Shaft left
        (int(hx + px * head_width / 2), int(hy + py * head_width / 2)),  # Head left
        (int(x2), int(y2)),                                      # Tip
        (int(hx - px * head_width / 2), int(hy - py * head_width / 2)),  # Head right
        (int(hx - px * shaft), int(hy - py * shaft)),            # Shaft right
        (int(x1 - px * shaft), int(y1 - py * shaft)),            # Back right
    ]

  def set_endpoints(self, x1, y1, x2, y2):
    self.points[:] = self.calculate_points(x1, y1, x2, y2)
    self.polygon.points = self.points

class Player:
  def __init__(self, i, group):
    self.index = i

    self.x = random.uniform(0, 128)
    self.y = random.uniform(0, 160)
    self.angle = 0

    self.area = []
    self.color = PLAYER_COLORS[i % len(PLAYER_COLORS)]

    self.circle = Circle(0, 0, PLAYER_RADIUS, fill=self.color)
    self.circle.x = int(self.x)
    self.circle.y = int(self.y)

    self.arrow = None

    self.update_arrow(group)

    self.sector = None

    self.discover_start = None
    self.discover_end = None

    group.append(self.circle)


  def update_arrow(self, group, x=None):
    if self.arrow:
      group.remove(self.arrow.polygon)
    
    if x == None:
      self.arrow = Arrow(int(self.x + PLAYER_RADIUS), int(self.y + PLAYER_RADIUS), int(self.x  + PLAYER_RADIUS + MOVE_BY * math.cos(self.angle)), int(self.y + PLAYER_RADIUS + MOVE_BY * math.sin(self.angle)), self.color);
    else: self.arrow = Arrow(int(x + PLAYER_RADIUS), int(self.y + PLAYER_RADIUS), int(x  + PLAYER_RADIUS + MOVE_BY * math.cos(self.angle)), int(self.y + PLAYER_RADIUS + MOVE_BY * math.sin(self.angle)), self.color);
 
    group.append(self.arrow.polygon)
  
  def rotate(self, add, group):
      global sector_draw_layer

      if current_stage == "Change":
        return
      self.angle += add * STEP

      if current_stage == "Discover":
        if (not self.discover_start == None) and (self.discover_end == None):
          if abs(self.discover_start - self.angle) >= MAX_DISCOVER_WIDTH:
            if self.discover_start < self.angle: self.angle = self.discover_start + MAX_DISCOVER_WIDTH
            if self.discover_start > self.angle: self.angle = self.discover_start - MAX_DISCOVER_WIDTH

          if not abs(self.discover_start - self.angle) < STEP:
            if self.sector:
              sector_draw_layer -= 1
              group.remove(self.sector.polygon)
              
            self.sector = Sector(self.x + PLAYER_RADIUS, self.y + PLAYER_RADIUS, self.discover_start, self.angle, 0x292b3d, group)
      
      self.update_arrow(group)


  def submit(self, group):
    global current_stage, current_player, change_player_text

    if current_stage == "Discover":
      if self.discover_start == None:
        # Set the discover start
        self.discover_start = self.angle

      elif abs(self.discover_start - self.angle) > STEP: 
        # Set the discover end
        self.discover_end = self.angle          

        sector = Sector(self.x + PLAYER_RADIUS, self.y + PLAYER_RADIUS, self.discover_start, self.discover_end, AREA_COLORS[self.index % len(AREA_COLORS)], group)
        self.area.append(sector)

        # Check if you've hit any players
        has_hit = False
        for player in players:
          if player.index != self.index:
            if sector.is_colliding(player, group):
              player.circle.x = int(player.x)
              if change_player_text in group: group.remove(change_player_text)
              change_player_text = Label(
                terminalio.FONT,
                text= COLOR_NAME[player.index % len(COLOR_NAME)]+" has died!",
                color=0xFFFFFF,
                x=10,
                y=20
              )

              group.append(change_player_text)
              has_hit = True
              # players.remove(player)

              print("GOOD JOB: COLLISION")

        if not has_hit:
          # Reset variables
          self.discover_start = None
          self.discover_end = None

          current_stage = "Move"
        else: current_stage = "Dead"

      self.update_arrow(group)
    elif current_stage == "Move":
      # Update the acctual player
      self.x += MOVE_BY * math.cos(self.angle)
      self.y += MOVE_BY * math.sin(self.angle)

      # Check if you've hit any areas 
      has_hit = False
      for player in players:
        if player.index != self.index:
          for sector in player.area:
            if sector.is_colliding(self, group):
              if change_player_text in group: group.remove(change_player_text)
              change_player_text = Label(
                terminalio.FONT,
                text= "You have died!",
                color=0xFFFFFF,
                x=10,
                y=20
              )

              group.append(change_player_text)
              has_hit = True
              # players.remove(player)
              print("WHOOPS: HIT AN AREA")

      if not has_hit:
        # Update the sprite
        self.circle.x = int(self.x)
        self.circle.y = int(self.y)

        # Reset the angle
        self.angle = 0    
        self.circle.x = 1000

        self.update_arrow(group, 1000)

        current_stage = "Change"

        if change_player_text in group: group.remove(change_player_text)

        change_player_text = Label(
          terminalio.FONT,
          text= COLOR_NAME[((self.index+1) % len(players)) % len(COLOR_NAME)]+"'s turn!",
          color=0xFFFFFF,
          x=10,
          y=20
        )

        group.append(change_player_text)
      else: current_stage = "Dead"
    elif current_stage == "Change":
      current_player += 1
      current_player = current_player % len(players)

      # Hide all other players by placing them off the screen
      for player in players:
        if player.index != current_player:
          player.circle.x = 1000
          player.update_arrow(group, 1000)
        else:
          player.circle.x = int(player.x)
          player.update_arrow(group)

      group.remove(change_player_text)
      current_stage = "Discover"  
    elif current_stage == "Dead":
      print("Oh No!")
def first_round(group):
  for player in players:
        if player.index != current_player:
          player.circle.x = 1000
          player.update_arrow(group, 1000)
        else:
          player.circle.x = int(player.x)
          player.update_arrow(group)


def update(group):
  global change_player_text

def spawn(group):
  for i in range(0, players_amount):
    players.append(Player(i, group))
