from pygame.sprite import Sprite, Group
from pygame.mask import from_surface
from pygame.image import load
from os.path import join as os_join
from math import cos, sin, pi, sqrt, atan
from random import uniform


# class Unit(Sprite):
class Unit:
    def __init__(self, bases=(1, 2, 3), contains=(100, 100), coords=(0, 0), destiny=1, distance=10, image="./data/unit.png",
                 index=0, radius=1, rotation=pi, speed=(1), sprites_group=Group(), unit_type=0, dict_converted=None):

        self.points = dict({*map(lambda x: (x, distance + 1), bases)})

        # super().__init__(sprites_group)

        self.generators = ['B']
        self.getters = ['A']

        self.contains = contains
        self.coords = coords
        self.destiny = destiny
        self.distance = distance
        self.index = index
        self.radius = radius
        self.rotation = rotation
        self.speed = speed
        self.unit_type = unit_type
        self.resource = 0

        # счётчик сигналов принимаемых на обработку
        self.speaking = 0
        self.max_speaking = 10

        if dict_converted is not None:
            for key, value in dict_converted.items():
                setattr(self, key, value)



    def check_requests(self, units: set, kinds_of_bases: list):
        for another_unit in units - {self}:

            # если сигналов на обработке больше максимального значения - перестаём спрашивать
            if self.speaking >= self.max_speaking:
                break

            if sqrt((another_unit.coords[0] - self.coords[0]) ** 2 + (
                    another_unit.coords[1] - self.coords[1]) ** 2) < self.distance:

                self.speaking += 1

                for key in kinds_of_bases:
                    self.listen(units, another_unit, key)


    def check_responses(self, units: set, base_kind):
        for another_unit in units - {self}:
            if ((another_unit.coords[0] - self.coords[0]) ** 2 + (
                    another_unit.coords[1] - self.coords[1]) ** 2) ** 0.5 < self.distance:

                another_unit.speaking += 1

                another_unit.listen(units, self, base_kind )
                # another_unit.check_responses(units, base_kind)


    def check_collides(self, units: set, bases: list, kinds_of_bases: list, walls: list):
        for base in bases:
            if sqrt(((self.coords[0] + self.radius / 2) - base.coords[0]) ** 2 +
                    ((self.coords[1] + self.radius / 2) - base.coords[1]) ** 2) <= base.radius + self.radius:
                self.encounter(base)

                # not done, yet

                # self.check_responses(units, base.kind)
                # self.check_requests(units, kinds_of_bases)


        for wall in walls:
            if wall.kind != 0:
                a = ((self.coords[0] - wall.first_point[0]) ** 2 +
                     (self.coords[1] - wall.first_point[1]) ** 2) ** 0.5
                b = ((self.coords[0] - wall.second_point[0]) ** 2 +
                     (self.coords[1] - wall.second_point[1]) ** 2) ** 0.5
                c = wall.length
                p = (a + b + c) / 2
                s = (p * (p - a) * (p - b) * (p - c)) ** 0.5
                path = s / c
                if path <= wall.width + self.radius and \
                        (wall.first_point[0] < self.coords[0] < wall.second_point[0] or
                         wall.first_point[0] > self.coords[0] > wall.second_point[0]) and \
                        (wall.first_point[1] < self.coords[1] < wall.second_point[1] or
                         wall.first_point[1] > self.coords[1] > wall.second_point[1]):
                    self.rotation += pi

    def encounter(self, base):
        self.points[base.kind] = 0
        if base.kind == self.destiny:
            if base.kind in self.generators and base.resource >= 1:
                base.resource -= 1
                self.resource += 1
            elif base.kind in self.getters and self.resource >= 1:
                self.resource -= 1
                base.resource += 1
            self.destiny = base.next
            self.rotation = (self.rotation + pi) % (2 * pi)


    def listen(self, units, unit, base_kind):
        if self.points[base_kind] > unit.points[base_kind] + self.distance * 1:
            self.points[base_kind] = unit.points[base_kind] + self.distance

            if base_kind == self.destiny:
                dx = unit.coords[0] - self.coords[0] 
                dy = unit.coords[1] - self.coords[1]

                # dx = self.coords[0] - unit.coords[0] 
                # dy = self.coords[1] - unit.coords[1]

                if dx == 0:
                    dx = 0.00000001

                # self.rotation = atan(dy / dx) + pi % (2 * pi)
                self.rotation = atan(dy / dx)

                if 0 > dx:
                    pass
                    self.rotation = (self.rotation + pi) % (2 * pi)

                if self.rotation < 0:
                    self.rotation = 2 * pi + self.rotation


                # print('I' if dx > 0 and dy > 0 else 'II' if dx < 0 and dy > 0 else 'III' if dx < 0 and dy < 0 else 'IV', "->", 'I' if 0 < self.rotation < pi / 2 else 'II' if pi / 2 < self.rotation < pi else 'III' if pi < self.rotation < 3 * pi / 2 else 'IV' if 3 * pi / 2 < self.rotation < 2 * pi else "bonk", self.rotation)

            # В этом нет нужды.
            # было перенесено в метод self.check_responses
            self.check_responses(units, base_kind)

    def move(self):
        dx = self.speed * cos(self.rotation)
        dy = self.speed * sin(self.rotation)

        if self.coords[0] + dx + self.radius >= self.contains[0] or self.coords[0] + dx <= self.radius:
            self.rotation = pi - self.rotation
            dx = self.speed * cos(self.rotation)

        if self.coords[1] + dy + self.radius >= self.contains[1] or self.coords[1] + dy <= self.radius:
            self.rotation = 2 * pi - self.rotation
            dy = self.speed * sin(self.rotation)

        self.coords = (self.coords[0] + dx, self.coords[1] + dy)
        self.rotation = (self.rotation + pi / 144 * uniform(-1, 1)) % (2 * pi)
        for key in self.points.keys():
            self.points[key] = self.points[key] + 1

    def update(self, units: list, bases: list, kinds_of_bases: list, walls: list):
        self.move()
        self.speaking = 0
        self.check_collides(set(units), bases, kinds_of_bases, walls)
        self.check_requests(set(units), kinds_of_bases)
        print(self.speaking)


