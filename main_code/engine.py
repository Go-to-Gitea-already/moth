import math
from random import choice, uniform, random
from main_code.unit import Unit
from main_code.base import Base
from main_code.menu import Menu
from main_code.wall import Wall
import pygame


class Engine:

    units = list()
    bases = list()
    walls = list()
    sprites = list()

    def __init__(self, width: int, height: int, count_of_units: int, count_of_bases: int, kinds_of_bases: list,
                 radius_of_base: float, unit_radius: float, units_speed: float, distance: float):
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

    def generate(self):
        self.units = list()
        self.bases = list()
        self.walls = list()

        contains_x, contains_y = self.width, self.height

        image = './data/spaceship.png'

        for i in range(self.count_of_units):

            coords = (random() * self.width, random() * self.height)
            self.units.append(Unit(self.kinds_of_bases, {'x': contains_x, 'y': contains_y}, coords, "A",
                                   self.distance, image, i, self.unit_radius, random() * 2 * math.pi,
                                   random() * self.units_speed / 5 * 4 + self.units_speed / 5, self.all_sprites, 0))

        for i in range(self.count_of_bases):
            coords = (random() * self.width, random() * self.height)
            kind = choice(self.kinds_of_bases)
            self.bases.append(Base(coords, kind, choice(list({*self.kinds_of_bases} - {kind})), i, self.radius_of_base))

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
            coords = (unit.coords["x"], unit.coords["y"])
            rect = (*coords, unit.radius * 2, unit.radius * 2)
            rotation = -unit.rotation - math.pi / 2
            image = pygame.transform.rotate(self.sprites[unit.unit_type], rotation * 180 / math.pi)
            self.screen.blit(image, rect)

    def start(self):

        self.screen = pygame.display.set_mode((self.width, self.height))

        start_menu = Menu(self.screen, {"start": lambda: print("game started!")})

        UNIT_UPDATE = pygame.USEREVENT + 4
        pygame.time.set_timer(UNIT_UPDATE, 50)

        running = True
        moving_of_base = False
        wall_building = False
        take = None
        moved_base = None
        wall_coord = None
        wall_index = None

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == UNIT_UPDATE:
                    for unit in self.units:
                        unit.update(self.units, self.bases, self.kinds_of_bases, self.walls)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        take = (event.pos[0], event.pos[1])
                        for base in self.bases:
                            x, y = base.coords[0], base.coords[0]
                            if x - base.radius < take[0] < x + base.radius and \
                                    y - base.radius < take[1] < y + base.radius:
                                moving_of_base = True
                                moved_base = base
                                take = (take[0] - x, take[1] - y)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        moving_of_base = False
                        take = None
                    if event.button == 1:
                        if wall_building:
                            if self.walls[wall_index].length >= 1:
                                self.walls[wall_index] = Wall(wall_coord, (event.pos[0], event.pos[1]), 10, 1)
                        else:
                            wall_coord = (event.pos[0], event.pos[1])
                            wall_index = len(self.walls)
                            self.walls.append(Wall(wall_coord, (event.pos[0], event.pos[1]), 10, 0))

                        wall_building = not wall_building

                if event.type == pygame.MOUSEMOTION and moving_of_base:
                    moved_base.move(event.pos[0] - take[0], event.pos[1] - take[1])

                if event.type == pygame.MOUSEMOTION and wall_building:
                    self.walls[wall_index] = Wall(wall_coord, (event.pos[0], event.pos[1]), 10, 0)

            self.render(self.screen)
            pygame.display.flip()
