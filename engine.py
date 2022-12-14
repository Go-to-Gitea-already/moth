import math
from random import random
from random import choice, uniform, random
from unit import Unit
from base import Base
import pygame


class Engine:
    units = list()
    bases = list()

    def __init__(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list, radius_of_base: float, units_size: float, units_speed: float, sim_speed: int, distance: float):
        self.units_speed = units_speed
        self.width = width
        self.height = height
        self.distance = distance
        self.kinds_of_bases = kinds_of_bases
        self.point_radius = radius_of_base
        self.generate(width, height, count_of_units, count_of_bases, kinds_of_bases, radius_of_base, units_size)


    def generate(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list,
                 radius_of_base: float, size_of_unit: float):
        self.units = list()
        self.bases = list()
        for i in range(count_of_units):
            coords = {'x': random() * width / 7 * 1.5 + width / 7 * 2.75, 'y': random() * height / 5 * 1.5 + height / 5 * 1.75}
            self.units.append(Unit(coords, random() * 2 * math.pi, "A",
                                   kinds_of_bases, i, {'x': width, 'y': height}, self.distance, random() * self.units_speed / 5 * 4 + self.units_speed / 5))

        coords = {'x': width / 7 * 2, 'y': height / 3 * 1}
        self.bases.append(Base(coords, 'A', 'B', 1, radius_of_base))

        coords = {'x': width / 7 * 2, 'y': height / 3 * 2}
        self.bases.append(Base(coords, 'A', 'B', 1, radius_of_base))

        coords = {'x': width / 7 * 5, 'y': height / 10 * 5}
        self.bases.append(Base(coords, 'B', 'A', 1, radius_of_base))

        # for i in range(count_of_bases):
        #    coords = {'x': random() * width, 'y': random() * height}
        #    kind = choice(kinds_of_bases)
        #    self.bases.append(Base(coords, kind, choice(list({*kinds_of_bases} - {kind})), i, radius_of_base,
        #                           self.graphics.new_image(coords, radius_of_base * 2, 'yellow')))


    def check_encounter(self, unit: Unit):
        for base in self.bases:
            if math.sqrt((unit.coords['x'] - base.coords['x']) ** 2 +
                         (unit.coords['y'] - base.coords['y']) ** 2) <= base.radius:
                Engine.encounter(unit, base)

                # not done, yet
                self.check_responses(unit, base.kind)
                self.check_requests(unit)


    def check_responses(self, unit, key):
        for another_unit in set(self.units) - {unit}:
            if ((another_unit.coords['x'] - unit.coords['x']) ** 2 + (
                    another_unit.coords['y'] - unit.coords['y']) ** 2) ** 0.5 < self.distance:
                self.listen(another_unit, unit, key)


    def check_requests(self, unit):
        for another_unit in set(self.units) - {unit}:
            if math.sqrt((another_unit.coords['x'] - unit.coords['x']) ** 2 + (
                    another_unit.coords['y'] - unit.coords['y']) ** 2) < self.distance:
                for key in self.kinds_of_bases:
                    self.listen(unit, another_unit, key)


    def listen(self, unit, unit2, key):
        if unit.points[key] > unit2.points[key] + unit.distance:
            unit.points[key] = unit2.points[key] + unit.distance

            if key == unit.destiny:
                dx = unit2.coords['x'] - unit.coords['x']
                dy = unit2.coords['y'] - unit.coords['y']
                unit.rotation = math.atan(dy / dx)
                if dx < 0:
                    unit.rotation = (unit.rotation + math.pi) % (2 * math.pi)
            self.check_responses(unit, key)
#             unit.image[2].lines.append(
#                 unit.image[0].create_line((unit2.coords['x'], unit2.coords['y']),
#                                           (unit.coords['x'], unit.coords['y']),
#                                           fill='green' if key == 'A' else 'blue'))


    def encounter(unit, base):
        unit.points[base.kind] = 0
        if base.kind == unit.destiny:
            unit.destiny = base.next
            unit.rotation = (unit.rotation + math.pi) % (2 * math.pi)


    def forward(unit):
        dx = unit.speed * math.cos(unit.rotation)
        dy = unit.speed * math.sin(unit.rotation)
        if unit.coords['x'] + dx >= unit.contains['x'] or unit.coords['y'] + dy >= unit.contains['y'] or \
                unit.coords['x'] + dx <= 0 or unit.coords['y'] + dy <= 0:
            unit.rotation = (unit.rotation + math.pi) % (2 * math.pi)
            dx = unit.speed * math.cos(unit.rotation)
            dy = unit.speed * math.sin(unit.rotation)
        unit.coords['x'] += dx
        unit.coords['y'] += dy
        # unit.rotation = (unit.rotation + math.pi / 144 * uniform(-1, 1)) % (2 * math.pi)
        for key in unit.points.keys():
            unit.points[key] = unit.points[key] + 1
       

    def timer_tick(self):
        for unit in self.units:
            Engine.forward(unit)
            self.check_encounter(unit)


    UNIT_COLOR = pygame.Color("red")
    BASE_COLOR = pygame.Color("green")

    def render(self, screen):
        screen.fill((0, 0, 0))
        for unit in self.units:
            coords = (unit.coords["x"], unit.coords["y"])
            pygame.draw.circle(screen, self.UNIT_COLOR, coords, 2)



    def start(self):

        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()

        TIMER_TICK = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMER_TICK, 50)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == TIMER_TICK:
                    self.timer_tick()

            self.render(screen)
            pygame.display.flip()
            














