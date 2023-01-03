import math


class Unit:

    def __init__(self, coords: dict, rotation: float, destiny, bases: list, index: int, contains: dict,
                 distance, speed: float, radius: float, unit_type=0):
        self.unit_type = unit_type
        self.coords = coords
        self.destiny = destiny
        self.rotation = rotation
        self.points = dict({*map(lambda x: (x, distance + 1), bases)})
        self.index = index
        self.contains = contains
        self.distance = distance
        self.speed = speed
        self.radius = radius
