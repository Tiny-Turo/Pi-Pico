import math

AREA = 10

def calculate_radius_of_sector(angle):
  radius = math.pow((2 * AREA) / angle, 1/2)
  return radius


