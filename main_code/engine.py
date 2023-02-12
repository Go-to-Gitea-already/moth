import math
import json
from random import choice, uniform, random
from main_code.unit import Unit
from main_code.base import Base
from ui.buttons import Buttons as Menu
from ui.drop_down_menu import DropDownMenu
from main_code.wall import Wall

import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Generator:
    def __init__(self, name, **kvargs):
        self.name = name
        self.params = kvargs

    def generate(self, constructor, **kvargs):

        args = self.params

        for a in kvargs.keys():
            if args.get(a) is None:
                args[a] = kvargs[a]

        print(self.name)
        print(args.get("speed"))
        print(self.params.get("speed"))
        print(kvargs.get("speed"))

        # print(s, args)

        return constructor(**args)
    
    def set_params(self, **kvargs):
        self.params = kvargs

    def get_params(self):
        return self.params


class Engine:

    units = list()
    bases = list()
    walls = list()
    sprites = list()

    def __init__(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list,
                 radius_of_base: float, unit_radius: float, units_speed: float, distance: float):

        pygame.init()

        self.pause = False

        self.screen = None
        self.units_speed = units_speed
        self.width = width
        self.height = height
        self.distance = distance
        self.kinds_of_bases = kinds_of_bases
        self.radius_of_base = radius_of_base
        self.unit_radius = unit_radius
        self.count_of_units = count_of_units
        self.count_of_bases = count_of_bases
        self.all_sprites = pygame.sprite.Group()

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.on_timer_tick = list()

        self.unit_types = list()

        self.unit_costs = {
            0: 10,
            1: 100
        }

        self.resource = 0

        self.generators = ['B']
        self.getters = ['A']

        self.space = load_image("space.jpg")

    def generate(self):
        self.units = list()
        self.bases = list()
        self.walls = list()

        contains_x, contains_y = self.width, self.height

        unit_image = './data/spaceship.png'
        base_image = './data/red_spaceship.png'

        # дефолтный тип юнита
        self.unit_types[0] = Generator(bases=self.kinds_of_bases, destiny="A", distance=self.distance, image=unit_image,
                 radius=self.unit_radius, sprites_group=self.all_sprites, unit_type=0)

        unit_type = 0

        for i in range(self.count_of_units):

            coords = (random() * self.width, random() * self.height)

            unit = self.unit_types[0].generate(Unit,
                                       contains={'x': contains_x, 'y': contains_y}, coords=coords,
                                       index=i, rotation=random() * 2 * math.pi,
                                       speed=random() * self.units_speed / 5 * 4 + self.units_speed / 5)

#             self.units.append(Unit(self.kinds_of_bases, {'x': contains_x, 'y': contains_y}, coords, A",
#                                    self.distance, unit_image, i, self.unit_radius, random() * 2 * math.pi,
#                                    random() * self.units_speed / 5 * 4 + self.units_speed / 5, self.all_sprites, 0))

        for i in range(self.count_of_bases):
            coords = (random() * self.width, random() * self.height)
            kind = choice(self.kinds_of_bases)
            self.bases.append(Base(coords, kind, choice(list({*self.kinds_of_bases} - {kind})), i, self.radius_of_base))

    def timer_tick(self):
        for f in self.on_timer_tick:
            f()

    UNIT_COLOR = (0, 0, 255)
    BASE1_COLOR = (255, 128, 0)
    BASE2_COLOR = (255, 0, 0)
    BASE3_COLOR = (255, 255, 0)
    BASE4_COLOR = (255, 0, 255)
    WALL_COLOR = (255, 0, 128)

    def render(self, screen):

        screen.blit(self.space, (0, 0))

        for wall in self.walls:
            pygame.draw.line(screen, self.WALL_COLOR, wall.first_point, wall.second_point, wall.width)

        for base in self.bases:
            coords = (base.coords[0], base.coords[1])
            color = (255, 255, 255)
            if base.kind == 'A':
                color = self.BASE1_COLOR
            elif base.kind == 'B':
                color = self.BASE2_COLOR
            elif base.kind == 'C':
                color = self.BASE3_COLOR
            elif base.kind == 'D':
                color = self.BASE4_COLOR

            pygame.draw.circle(screen, color, coords, self.radius_of_base)

            color = (255, 255, 255)
            if base.next == 'A':
                color = self.BASE1_COLOR
            elif base.next == 'B':
                color = self.BASE2_COLOR
            elif base.next == 'C':
                color = self.BASE3_COLOR
            elif base.next == 'D':
                color = self.BASE4_COLOR

            pygame.draw.circle(screen, color, coords, self.radius_of_base / 2)

        for unit in self.units:
            coords = (unit.coords[0], unit.coords[1])
            rect = (*coords, unit.radius * 2, unit.radius * 2)
            rotation = -unit.rotation - math.pi / 2
            image = pygame.transform.rotate(self.sprites[unit.unit_type], rotation * 180 / math.pi)
            self.screen.blit(image, rect)


    def parse_to_dict(self, arr):
        return map(lambda x: x.__dict__, arr)


    def units_to_text(self):
        units_json = json.dumps(list(self.parse_to_dict(self.units)))
        return units_json


    def bases_to_text(self):
        bases_json = json.dumps(list(self.parse_to_dict(self.bases)))
        return bases_json


    def walls_to_text(self):
        walls_json = json.dumps(list(self.parse_to_dict(self.walls)))
        return walls_json

    
    def parse_from_dict(self, t, arr):
        return list(map(lambda x: t(dict_converted=x), arr))


    def units_from_json(self, text):
        self.units = self.parse_from_dict(Unit, json.loads(text))


    def bases_from_json(self, text):
        self.bases = self.parse_from_dict(Base, json.loads(text))


    def walls_from_json(self, text):
        self.walls = self.parse_from_dict(Wall, json.loads(text))


    def start(self):
        # нужно для нормального функционирования стартового меню
        self.events = pygame.event.get()

        TIMER_TICK = pygame.USEREVENT + 1
        self.running = True

        while self.running:
            #!
            self.events = pygame.event.get()
            self.render(self.screen)

            #!
            # запускаем всё остальное
            self.timer_tick()

            pygame.display.flip()
