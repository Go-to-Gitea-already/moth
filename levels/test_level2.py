import pygame.image

from main_code.engine import Engine
import math
from main_code.unit import Unit
from main_code.base import Base


class Field(Engine):
    def __init__(self):

        w = 600
        h = 600

        units_count = 221
        unit_radius = 6
        unit_speed = 3
        unit_hear_distance = 45

        bases_count = 4
        base_types = ['A', 'B']
        base_radius = 45

        super().__init__(w, h, units_count, bases_count, base_types, base_radius, unit_radius, unit_speed,
                         unit_hear_distance)
        self.generate()

    def generate(self):
        self.units = list()
        self.bases = list()

        self.sprites = list()

        self.sprites.append(pygame.image.load('./data/spaceship.png'))
        self.sprites.append(pygame.image.load('./data/red_spaceship.png'))

        contains_x, contains_y = self.width, self.height

        bungle = self.count_of_units // 11
        for i in range(11):
            rotate = (math.pi + math.pi / 20 * (i * 1)) % (2 * math.pi)

            for j in range(bungle):
                y_c = (contains_y - self.radius_of_base * -1.0) - (2 * self.radius_of_base - (self.radius_of_base + j)
                                                                   * math.sin(rotate))
                x_c = (contains_x - self.radius_of_base * -1.0) - (2 * self.radius_of_base - (self.radius_of_base + j)
                                                                   * math.cos(rotate))

                coords = {'x': x_c, 'y': y_c}
                speed = self.units_speed / 3 + self.units_speed / 3 * 2 / bungle * (j + 1)
                self.units.append(Unit(coords, rotate, "B",
                                       self.kinds_of_bases, i, {'x': contains_x, 'y': contains_y}, self.distance, speed,
                                       self.unit_radius))

        self.units.append(Unit({'x': 100, 'y': 100}, 0.000001, "B",
                               self.kinds_of_bases, 222, {'x': contains_x, 'y': contains_y}, self.distance,
                               self.units_speed, self.unit_radius, 1))
        coords = {'x': contains_x - (contains_x ** 2 / 2) ** 0.5, 'y': contains_y - (contains_y ** 2 / 2) ** 0.5}
        self.bases.append(Base(coords, 'B', 'A', 1, self.radius_of_base))

        coords = {'x': self.radius_of_base, 'y': contains_y - self.radius_of_base}
        self.bases.append(Base(coords, 'B', 'A', 1, self.radius_of_base))

        coords = {'x': contains_x - self.radius_of_base, 'y': self.radius_of_base}
        self.bases.append(Base(coords, 'B', 'A', 1, self.radius_of_base))

        coords = {'x': contains_x - self.radius_of_base, 'y': contains_y - self.radius_of_base}
        self.bases.append(Base(coords, 'A', 'B', 1, self.radius_of_base))
