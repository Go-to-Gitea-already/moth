import pygame.image
from main_code.engine import Engine, Generator
from main_code.base_level import InputUIDefineLevel
import math
from main_code.unit import Unit
from main_code.base import Base
from random import random


class Field(InputUIDefineLevel):
    def __init__(self):

        w = 600
        h = 600

        units_count = 221
        unit_radius = 6
        unit_speed = 3
        unit_hear_distance = 45

        bases_count = 4
        base_types = ('A', 'B')
        base_radius = 45

        super().__init__(w, h, units_count, bases_count, base_types, base_radius, unit_radius, unit_speed,
                         unit_hear_distance)
        self.generate()

    def generate(self):
        self.units = list()
        self.bases = list()

        self.sprites = list()

        im = pygame.image.load('./data/spaceship.png')
        im = pygame.transform.scale(im, (self.unit_radius, self.unit_radius))
        self.sprites.append(im)

        contains_x, contains_y = self.width, self.height

        bungle = self.count_of_units // 11

        unit_image = './data/spaceship.png'
        base_image = './data/red_spaceship.png'


        # дефолтный тип юнита
        self.unit_types.append(Generator('D', bases=self.kinds_of_bases, destiny="B", distance=self.distance, image=unit_image,
                 radius=self.unit_radius, sprites_group=self.all_sprites, unit_type=0))

        # не дефолтный тип юнита
        self.unit_types.append(Generator('S', bases=self.kinds_of_bases, destiny="B", distance=self.distance, image=unit_image,
                 radius=self.unit_radius, sprites_group=self.all_sprites, unit_type=0, speed=20))


        unit_type = 0


        for i in range(11):
            rotate = (math.pi + math.pi / 20 * (i * 1)) % (2 * math.pi)

            for j in range(bungle):
                y_c = (contains_y - self.radius_of_base * -1.0) - (2 * self.radius_of_base - (self.radius_of_base + j)
                                                                   * math.sin(rotate))
                x_c = (contains_x - self.radius_of_base * -1.0) - (2 * self.radius_of_base - (self.radius_of_base + j)
                                                                   * math.cos(rotate))

                speed = self.units_speed / 3 + self.units_speed / 3 * 2 / bungle * (j + 1)
                coords = (x_c, y_c)
                unit = self.unit_types[0].generate(Unit,
                                       contains=(contains_x, contains_y), coords=coords,
                                       index=i, rotation=random() * 2 * math.pi,
                                       speed=random() * self.units_speed / 5 * 4 + self.units_speed / 5)


                self.units.append(unit)
#                 self.units.append(Unit(self.kinds_of_bases, {'x': contains_x, 'y': contains_y}, coords, "A",
#                                        self.distance, unit_image, i, self.unit_radius, random() * 2 * math.pi,
#                                        speed, self.all_sprites, 0))

        coords = (contains_x - (contains_x ** 2 / 2) ** 0.5, contains_y - (contains_y ** 2 / 2) ** 0.5)
        self.bases.append(Base(coords, base_image, 1, 'B', 'A', self.radius_of_base, self.all_sprites))

        coords = (self.radius_of_base, contains_y - self.radius_of_base)
        self.bases.append(Base(coords, base_image, 1, 'B', 'A', self.radius_of_base, self.all_sprites))

        coords = (contains_x - self.radius_of_base, self.radius_of_base)
        self.bases.append(Base(coords, base_image, 1, 'B', 'A', self.radius_of_base, self.all_sprites))

        coords = (contains_x - self.radius_of_base, contains_y - self.radius_of_base)
        self.bases.append(Base(coords, base_image, 1, 'A', 'B', self.radius_of_base, self.all_sprites))
