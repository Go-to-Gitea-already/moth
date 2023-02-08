import math
from random import choice, uniform, random
from main_code.unit import Unit
from main_code.base import Base
from ui.buttons import Buttons as Menu
from ui.drop_down_menu import DropDownMenu
from main_code.wall import Wall

import pygame


class Generator:
    def __init__(self, name, **kvargs):
        self.name = name
        self.params = kvargs

    def generate(self, constructor, **kvargs):

        s = set(self.params.items()) | (set(kvargs.items()) - set(self.params.items()))
        args = dict(s)

        print(s, args)

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

        self.on_timer_tick = list()

        self.unit_types = list()

        self.unit_costs = {
            0: 10,
            1: 100
        }

        self.resource = 0

        self.generators = ['B']
        self.getters = ['A']

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
        screen.fill((0, 0, 0))

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

    def start(self):
        # нужно для нормального функционирования стартового меню
        self.events = pygame.event.get()

        self.screen = pygame.display.set_mode((self.width, self.height))

        start_menu = Menu(self, {"start": lambda: print("started")}, stop_main_process=True)

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
