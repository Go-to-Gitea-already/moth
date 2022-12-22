import math
from random import random
from random import choice, uniform, random
from engine.unit import Unit
from engine.base import Base
import pygame


class Engine:
    units = list()
    bases = list()

    def __init__(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list,
                 radius_of_base: float, unit_radius: float, units_speed: float, distance: float):
        self.units_speed = units_speed
        self.width = width
        self.height = height
        self.distance = distance
        self.kinds_of_bases = kinds_of_bases
        self.base_radius = radius_of_base
        self.unit_radius = unit_radius
        self.count_of_units = count_of_units


    def generate(self):
        self.units = list()
        self.bases = list()

        contains_x, contains_y = self.width, self.height
        for i in range(self.count_of_units):
#             coords = {'x': random() * radius_of_base + (contains_x - radius_of_base * 3), 
#                       'y': random() * radius_of_base + (contains_y - radius_of_base * 3)}

            coords = {'x': random() * contains_x, 'y': random() * contains_y}
            self.units.append(Unit(coords, random() * 2 * math.pi, "A",
                                   self.kinds_of_bases, i, {'x': contains_x, 'y': contains_y},
                                   self.distance, random() * self.units_speed / 5 * 4 + self.units_speed / 5, self.unit_radius))


        for i in range(self.count_of_bases):
           coords = {'x': random() * self.width, 'y': random() * self.height}
           kind = choice(self.kinds_of_bases)
           self.bases.append(Base(coords, kind, choice(list({*self.kinds_of_bases} - {kind})), i, self.radius_of_base))


    def check_encounter(self, unit: Unit):
        for base in self.bases:
            if math.sqrt((unit.coords['x'] - base.coords['x']) ** 2 +
                         (unit.coords['y'] - base.coords['y']) ** 2) <= base.radius + self.unit_radius:
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
        if unit.points[key] > unit2.points[key] + unit.distance * 1:
            unit.points[key] = unit2.points[key] + unit.distance

            if key == unit.destiny:
                dx = unit2.coords['x'] - unit.coords['x']
                dy = unit2.coords['y'] - unit.coords['y']
                if dx == 0:
                    dx = 0.00000001

                unit.rotation = math.atan(dy / dx)

                if dx < 0:
                    pass
                    unit.rotation = (unit.rotation + math.pi) % (2 * math.pi)

            self.check_responses(unit, key)


    def encounter(unit, base):
        unit.points[base.kind] = 0
        if base.kind == unit.destiny:
            unit.destiny = base.next
            cos = (base.coords['x'] - unit.coords['x']) / (base.radius + unit.radius * 2)

            unit.rotation = (unit.rotation + math.pi) % (2 * math.pi)

            # not done

#             angle = math.acos(cos)
#             if unit.coords['y'] < base.coords['y']:
#                 angle = math.pi * 2 - angle
# 
#             difference = unit.rotation - angle
#             unit.rotation = (unit.rotation + difference * 2) % (2 * math.pi)



    def forward(unit):
        dx = unit.speed * math.cos(unit.rotation)
        dy = unit.speed * math.sin(unit.rotation)

        if unit.coords['x'] + dx + unit.radius >= unit.contains['x'] or unit.coords['x'] + dx <= unit.radius:
            unit.rotation = math.pi - unit.rotation
            dx = unit.speed * math.cos(unit.rotation)
        
        if unit.coords['y'] + dy + unit.radius >= unit.contains['y'] or unit.coords['y'] + dy <= unit.radius:
            unit.rotation = 2 * math.pi - unit.rotation
            dy = unit.speed * math.sin(unit.rotation)

        unit.coords['x'] += dx
        unit.coords['y'] += dy
        unit.rotation = (unit.rotation + math.pi / 144 * uniform(-1, 1)) % (2 * math.pi)
        for key in unit.points.keys():
            # unit.points[key] = unit.points[key] + unit.speed
            unit.points[key] = unit.points[key] + 1
       

    def timer_tick(self):
        for unit in self.units:
            self.check_requests(unit)


    UNIT_COLOR = (0, 0, 255)
    BASE1_COLOR = (255, 128, 0)
    BASE2_COLOR = (255, 0, 0)
    BASE3_COLOR = (255, 255, 0)
    BASE4_COLOR = (255, 0, 255)

    def render(self, screen):
        screen.fill((0, 0, 0))

        for base in self.bases:
            coords = (base.coords["x"], base.coords["y"])
            color = (255, 255, 255)
            if base.kind == 'A':
                color = self.BASE1_COLOR
            elif base.kind == 'B':
                color = self.BASE2_COLOR
            elif base.kind == 'C':
                color = self.BASE3_COLOR
            elif base.kind == 'D':
                color = self.BASE4_COLOR

            pygame.draw.circle(screen, color, coords, self.base_radius)

            color = (255, 255, 255)
            if base.next == 'A':
                color = self.BASE1_COLOR
            elif base.next == 'B':
                color = self.BASE2_COLOR
            elif base.next == 'C':
                color = self.BASE3_COLOR
            elif base.next == 'D':
                color = self.BASE4_COLOR

            pygame.draw.circle(screen, color, coords, self.base_radius / 2)


        for unit in self.units:
            coords = (unit.coords["x"], unit.coords["y"])
            rect = (*coords, unit.radius * 2, unit.radius * 2)
            rotation = -(unit.rotation) - math.pi / 2
            image = pygame.transform.rotate(self.sprites[unit.type], rotation * 180 / math.pi)
            self.screen.blit(image, rect)



    def start(self):

        self.screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()

        TIMER_TICK = pygame.USEREVENT + 1
        MOVE_EVENT = pygame.USEREVENT + 2
        CHECK_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(TIMER_TICK, 200)
        pygame.time.set_timer(MOVE_EVENT, 50)
        pygame.time.set_timer(CHECK_EVENT, 100)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == TIMER_TICK:
                    self.timer_tick()

                elif event.type == MOVE_EVENT:
                    for unit in self.units:
                        Engine.forward(unit)

                elif event.type == CHECK_EVENT:
                    for unit in self.units:
                        self.check_encounter(unit)

            self.render(self.screen)
            pygame.display.flip()
