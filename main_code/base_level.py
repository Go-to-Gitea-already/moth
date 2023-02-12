from main_code.engine import *
from ui.buttons import Buttons
from ui.input import InputBox
import pygame

import shutil
from zipfile import ZipFile
import os

# from file_handler import *


class Variables:
    pass


pygame.font.init()


"""все связанное с вводом с клавиатуры и мыши располагается здесь, в родителях и наследниках. 
Также здесь расположено создание меню для спавна юнита"""
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
                print("not enoth resources")
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


"""все связанное со стандартными меню располагается здесь, в родителях и наследниках.
Kроме создания меню для спавна юнита"""
class GUIDefineLevel(Engine):
    def __init__(self):
        self.draw_variables = Variables()

        self.draw_variables.menus = list()

        
        # пихаем стартовое меню вместо старта **злобный смех**
        def start():
            self.call_main_menu()
        
        self.start = start


        # создание меню быстрых действий
        rect = pygame.Rect((0, 0), (0, 0))
        rect.left=self.width - 50
        rect.top=25
        rect.width=25
        rect.height=150
        self.draw_variables.action_menu = Buttons(self,
                                                  {'p': self.pause_game,
                                                   's': self.save_game,
                                                   'e': self.end_game}, 
                                                  is_static=True,
                                                  rect=rect,
                                                  button_w=25, button_h=25)
        # print(2)


    def call_main_menu(self):
        rect = pygame.Rect((0, 100), (self.width, self.height - 100))
        self.draw_variables.main_menu = Buttons(self, {"load": self.load_game,
                                                        "create": self.create_game,
                                                        "about": self.about,
                                                        "manual": self.manual,
                                                        "exit": exit},
                                                 stop_main_process=True, rect=rect)


    def resume(self):
        self.pause = False


    def pause_game(self):

        font = pygame.font.SysFont(None, 100)
        text = font.render("pause", True, (255, 128, 0))

        f = lambda: self.screen.blit(text, (self.width // 2 - 100, 50))

        self.pause = True

        rect = pygame.Rect((0, 150), (self.width, self.height - 100))
        self.draw_variables.pause_menu = Buttons(self, {"resume": self.resume,
                                                        "save": self.save_game,
                                                        "load": self.load_game,
                                                        "create": self.create_game,
                                                        "main menu": self.call_main_menu},
                                                 processes_on=[f],
                                                 stop_main_process=True, rect=rect)



    def save_game(self):
        input_box = InputBox(self, self.width // 2 - 80, self.height // 2 - 20, 160, 40)
        filename = "./saves/" + input_box.wait().rstrip("/").rstrip("\\") + ".lvl"

        if not os.path.exists("./saves/"):
            os.makedirs("./saves/")

        if not os.path.exists(filename):
            os.makedirs(filename)

            with (open(f"{filename}/units.json", "w") as units,
                  open(f"{filename}/bases.json", "w") as bases,
                  open(f"{filename}/walls.json", "w") as walls):

                units.write(self.units_to_text())
                bases.write(self.bases_to_text())
                walls.write(self.walls_to_text())

            shutil.make_archive(filename, 'zip', root_dir=filename)
            shutil.rmtree(filename)
            shutil.move(filename + ".zip", filename)

        return False


    def load_game(self):
        input_box = InputBox(self, self.width // 2 - 80, self.height // 2 - 20, 160, 40)
        filename = "./saves/" + input_box.wait().rstrip("/").rstrip("\\") + ".lvl"

        if not os.path.exists("./saves/"):
            os.makedirs("./saves/")

        if not os.path.exists(filename):
            os.makedirs(filename)

        with ZipFile(filename) as zipfile:
            with (zipfile.open('units.json', 'r') as units,
                  zipfile.open('bases.json', 'r') as bases,
                  zipfile.open('walls.json', 'r') as walls):

                self.units_from_json(units.read())
                self.bases_from_json(bases.read())
                self.walls_from_json(walls.read())


    def about(self):
        pass


    def manual(self):
        pass


    def end_game(self):
        self.running = False
        self.call_main_menu()


    def create_game(self):
        self.running = True

        self.generate()
        super().start()


"""все связанное с UI находится здесь, в родителях и наследниках"""
class UIDefineLevel(InputUIDefineLevel, GUIDefineLevel):
    def __init__(self):
        InputUIDefineLevel.__init__(self)
        GUIDefineLevel.__init__(self)
        self.on_timer_tick.append(self.UI_event_handle)


        font = pygame.font.SysFont(None, 25)

        def print_resouce_count():
            text = font.render(str(self.resource), True, (255, 128, 0))

            self.screen.blit(text, (25, 25))

        self.on_timer_tick.append(print_resouce_count)


    def UI_event_handle(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_game()


"""все связанное с логикой располагается здесь, в родителях и наследниках"""
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
            # print(event)
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



"""Шаблон для стандартного уровня. Здесь может определяться функционал связанный со всеми базовыми уровнями."""
class ComplexLevel(UIDefineLevel, LogicDefineLevel, Engine):
    def __init__(self, *args, **kvargs):
        Engine.__init__(self, *args, **kvargs)
        UIDefineLevel.__init__(self)
        LogicDefineLevel.__init__(self)


