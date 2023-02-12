import pygame
from threading import Thread

pygame.font.init()


class Buttons:
    def __init__(self, engine, choices: dict,
                 background_process=None, processes_on=None, processes_under=None, is_static=False, stop_main_process=False,
                 rect=None, button_w=200, button_h=50):

        self.engine = engine
        self.screen = engine.screen
        self.button_w = button_w
        self.button_h = button_h

        self.rect = rect if rect is not None else pygame.Rect((0, 0), self.screen.get_size())

        self.is_static = is_static
        self.stop_main_process = stop_main_process

        self.processes_on = processes_on
        self.processes_under = processes_under

#         self.background = Thread(target=background_process)
#         self.background.start()

#         self.background.terminate()

        self.make_choice(choices)

    def generate(self, main_color=(0, 0, 0), accent_color=(255, 128, 0)):
        self.main_color = main_color
        self.accent_color = accent_color

        x0 = self.rect.left
        x1 = self.rect.right

        x = self.rect.center[0]

        # print(x0, x, x1)

        y0 = self.rect.top
        y1 = self.rect.bottom

        # print(y0, self.rect.y, y1)

        l = len(self.choices)

        h = int(self.rect.height * 0.8 // l)

        self.choices_boxes = list()


        for text, y in zip(self.choices.keys(), range(y0 + int(h // 2), y1, h)):
            font = pygame.font.SysFont("monospace", int(self.button_h))

            label = font.render(text, 1, main_color)

            rect = label.get_rect()
            rect.width = self.button_w
            self.height = self.button_h
            rect.center = x, y

            self.choices_boxes.append((label, rect, text) ,)


    def draw(self):
        if self.screen is None:
            self.screen = self.engine.screen

        for box in self.choices_boxes:
            rect = pygame.Rect(box[1])

            w = 2
            rect.top -= w
            rect.left -= w
            rect.height += w * 2
            rect.width += w * 2

            pygame.draw.rect(self.screen, self.main_color, rect)

            pygame.draw.rect(self.screen, self.accent_color, pygame.Rect(box[1]))

            self.screen.blit(box[0], box[1])


    def check_buttons(self, x, y):
        for box in self.choices_boxes:
            rect = box[1]
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                self.choices[box[2]]()

                if not self.is_static:
                    self.running = False

                return True

        return False

    
    def make_all(functions):
        for f in functions:
            f()


    def make_choice(self, choices: dict):
        self.choices = choices
        self.generate()

        self.running = True

        def on_timer_tick():
            if self.processes_under is not None:
                Buttons.make_all(self.processes_under)

            if self.stop_main_process:
                events = pygame.event.get()

            else:
                events = self.engine.events

            for e in events:
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = e.pos

                    # ах шит
                    if self.check_buttons(x, y):
                        if not self.stop_main_process:
                            self.engine.events.remove(e)

            self.draw()

            if self.processes_on is not None:
                Buttons.make_all(self.processes_on)

            # говнокод
            if not (self.running or self.stop_main_process):
                self.engine.on_timer_tick.remove(on_timer_tick)

        if self.stop_main_process:
            while self.running:
                self.screen.fill(self.main_color)
                on_timer_tick()
                pygame.display.flip()

        else:
            self.engine.on_timer_tick.append(on_timer_tick)

