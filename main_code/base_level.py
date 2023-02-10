from main_code.engine import *
from ui.buttons import Buttons
import pygame


class Variables:
    pass


class InputUIDefineLevel(Engine):
    def __init__(self):
        self.input_variables = Variables()

        self.input_variables.moving_of_base = False
        self.input_variables.wall_building = False
        self.input_variables.take = None
        self.input_variables.moved_base = None
        self.input_variables.wall_coord = None
        self.input_variables.wall_index = None

        self.on_timer_tick.append(self.input_event_handle)


    def input_event_handle(self):
        for event in self.events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # проверка на по то, покрывает ли курсор базу
                    self.input_variables.take = (event.pos[0], event.pos[1])
                    for base in self.bases:
                        x, y = base.coords
                        if x - base.radius < self.input_variables.take[0] < x + base.radius and \
                                y - base.radius < self.input_variables.take[1] < y + base.radius:
                            self.input_variables.moving_of_base = True
                            self.input_variables.moved_base = base
                            self.input_variables.take = (self.input_variables.take[0] - x, self.input_variables.take[1] - y)
                            break

                    else:
                        pass
 
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.input_variables.moving_of_base = False
                    self.input_variables.take = None

                if event.button == 3:
                    if self.input_variables.wall_building:
                        self.walls[self.input_variables.wall_index] = Wall(self.input_variables.wall_coord, (event.pos[0], event.pos[1]), 1, self.all_sprites, 2)
                    else:
                        self.input_variables.wall_coord = (event.pos[0], event.pos[1])
                        self.input_variables.wall_index = len(self.walls)
                        self.walls.append(Wall(self.input_variables.wall_coord, (event.pos[0], event.pos[1]), 0, self.all_sprites, 2))

                    self.input_variables.wall_building = not self.input_variables.wall_building

            if event.type == pygame.MOUSEMOTION and self.input_variables.moving_of_base:
                self.input_variables.moved_base.move(event.pos[0] - self.input_variables.take[0], event.pos[1] - self.input_variables.take[1])

            if event.type == pygame.MOUSEMOTION and self.input_variables.wall_building:
                self.walls[self.input_variables.wall_index] = Wall(self.input_variables.wall_coord, (event.pos[0], event.pos[1]), 0, self.all_sprites, 2)

            # клавиши
            if event.type == pygame.KEYDOWN:

                # спавн юнита
                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    coords = pos
                    self.spawn_unit(coords)


    def spawn_unit(self, coords):
        contains_x, contains_y = self.width, self.height

        def spawn(unit_type):
            if self.resource < self.unit_costs[unit_type.params["unit_type"]]:
                return False

            self.resource -= self.unit_costs[unit_type.params["unit_type"]]
            self.units.append(unit_type.generate(Unit,
                                                    contains=(contains_x, contains_y), coords=coords,
                                                    index=len(self.units), rotation=random() * 2 * math.pi,
                                                    speed=random() * self.units_speed / 5 * 4 + self.units_speed / 5))

        options = dict(map(lambda x: (x.name, lambda: spawn(x)),
                           self.unit_types))

        print(self.unit_types)
        print(options.items())

        DropDownMenu(self, options, *coords)


class GUIDefineLevel(Engine):
    def __init__(self, *args, **kvargs):
        self.draw_variables = Variables()

        self.draw_variables.menus = list()

        # создание меню быстрых действий
        rect = pygame.Rect((0, 0), (0, 0))
        rect.left=self.height - 50
        rect.top=25
        rect.width=25
        rect.height=150
        self.draw_variables.action_menu = Buttons(self,
                                                  {'1': lambda: print(1),
                                                   '2': lambda: print(2),
                                                   '3': lambda: print(3)}, 
                                                  is_static=True,
                                                  rect=rect,
                                                  button_w=25, button_h=25)


class LogicDefineLevel(Engine):
    def __init__(self):
        self.logic_variables = Variables()

        self.logic_variables.MOVE_EVENT = pygame.USEREVENT + 2
        self.logic_variables.CHECK_EVENT = pygame.USEREVENT + 3
        self.logic_variables.UNIT_UPDATE = pygame.USEREVENT + 4
        self.logic_variables.GENERATE_RES = pygame.USEREVENT + 5

        pygame.time.set_timer(self.logic_variables.MOVE_EVENT, 50)
        pygame.time.set_timer(self.logic_variables.CHECK_EVENT, 100)
        pygame.time.set_timer(self.logic_variables.UNIT_UPDATE, 50)
        pygame.time.set_timer(self.logic_variables.GENERATE_RES, 1000)

        self.on_timer_tick.append(self.logic_event_handle)


    def logic_event_handle(self):
        for event in self.events:

            if event.type == self.logic_variables.UNIT_UPDATE:
                for unit in self.units:
                    unit.update(self.units, self.bases, self.kinds_of_bases, self.walls)

            if event.type == self.logic_variables.GENERATE_RES:
                for base in self.bases:
                    base.update()
                    if base.kind in self.getters:
                        self.resource += base.resource
                        base.resource = 0
                print(self.resource)

            if event.type == pygame.QUIT:
                self.running = False

#             if event.type == self.logic_variables.MOVE_EVENT:
#                 for unit in self.units:
#                     forward(unit)

#             if event.type == self.logic_variables.CHECK_EVENT:
#                 for unit in self.units:
#                     self.check_encounter(unit)
# 
#                 for unit in self.units:
#                     self.check_requests(unit)
#



class ComplexLevel(InputUIDefineLevel, GUIDefineLevel, LogicDefineLevel, Engine):
    def __init__(self, *args, **kvargs):
        Engine.__init__(self, *args, **kvargs)
        InputUIDefineLevel.__init__(self)
        GUIDefineLevel.__init__(self)
        LogicDefineLevel.__init__(self)

