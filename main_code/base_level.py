from main_code.engine import *
import pygame


class Variables:
    pass


class InputUIDefineLevel(Engine):
    def __init__(self, *args, **kvargs):
        super().__init__(*args, **kvargs)

        pygame.init()
        self.input_variables = Variables()
        self.input_variables.MOVE_EVENT = pygame.USEREVENT + 2
        self.input_variables.CHECK_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.input_variables.MOVE_EVENT, 50)
        pygame.time.set_timer(self.input_variables.CHECK_EVENT, 100)

        self.input_variables.moving_of_base = False
        self.input_variables.wall_building = False
        self.input_variables.take = None
        self.input_variables.moved_base = None
        self.input_variables.wall_coord = None
        self.input_variables.wall_index = None

        self.on_timer_tick.append(self.event_handle)


    def event_handle(self):
        for event in self.events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # проверка на по то, покрывает ли курсор базу
                    self.input_variables.take = (event.pos[0], event.pos[1])
                    for base in self.bases:
                        x, y = base.coords['x'], base.coords['y']
                        if x - base.radius < self.input_variables.take[0] < x + base.radius and \
                                y - base.radius < self.input_variables.take[1] < y + base.radius:
                            self.input_variables.moving_of_base = True
                            self.input_variables.moved_base = base
                            self.input_variables.take = (self.input_variables.take[0] - x, self.input_variables.take[1] - y)
                            break

                    else:
                        pass


            if event.type == pygame.QUIT:
                self.running = False

            if event.type == self.input_variables.MOVE_EVENT:
                for unit in self.units:
                    forward(unit)

            if event.type == self.input_variables.CHECK_EVENT:
                for unit in self.units:
                    self.check_encounter(unit)

                for unit in self.units:
                    self.check_requests(unit)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.input_variables.moving_of_base = False
                    self.input_variables.take = None

                if event.button == 3:
                    if self.input_variables.wall_building:
                        self.walls[self.input_variables.wall_index] = Wall(self.input_variables.wall_coord, (event.pos[0], event.pos[1]), 2, 1)
                    else:
                        self.input_variables.wall_coord = (event.pos[0], event.pos[1])
                        self.input_variables.wall_index = len(self.walls)
                        self.walls.append(Wall(self.input_variables.wall_coord, (event.pos[0], event.pos[1]), 2, 0))

                    self.input_variables.wall_building = not self.input_variables.wall_building

            if event.type == pygame.MOUSEMOTION and self.input_variables.moving_of_base:
                base_moving(self.input_variables.moved_base, event.pos[0] - self.input_variables.take[0], event.pos[1] - self.input_variables.take[1])

            if event.type == pygame.MOUSEMOTION and self.input_variables.wall_building:
                self.walls[self.input_variables.wall_index] = Wall(self.input_variables.wall_coord, (event.pos[0], event.pos[1]), 2, 0)

            # клавиши
            if event.type == pygame.KEYDOWN:

                # спавн юнита
                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    coords = {'x': pos[0], 'y': pos[1]}
                    self.spawn_unit(coords)


    def spawn_unit(self, coords):
        contains_x, contains_y = self.width, self.height

        DropDownMenu(self, {
            '0': lambda: self.units.append(Unit(coords, random() * 2 * math.pi, 
                                                "A", self.kinds_of_bases, len(self.units), 
                                                {'x': contains_x, 'y': contains_y}, 
                                                self.distance, 
                                                random() * self.units_speed / 5 * 4 + self.units_speed / 5,
                                                self.unit_radius)),
            '1': lambda: self.units.append(Unit(coords, random() * 2 * math.pi, 
                                                "A", self.kinds_of_bases, len(self.units), 
                                                {'x': contains_x, 'y': contains_y}, 
                                                self.distance, 
                                                random() * self.units_speed / 5 * 4 + self.units_speed / 5,
                                                self.unit_radius, 1)),
            '2': lambda: print(2),
            '3': lambda: print(3)},
            coords['x'], coords['y'])


        pass


class DrawDefineLevel(Engine):
    pass

