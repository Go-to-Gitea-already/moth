import pygame
pygame.font.init()


class Menu:
    def __init__(self, screen, choices: dict, button_w=200, button_h=50):
        self.screen = screen

        self.x_c, self.y_c = screen.get_size()
        self.button_w = button_w
        self.button_h = button_h

        self.make_choice(choices)

    def generate(self, main_color=(0, 0, 0), accent_color=(255, 128, 0)):
        self.main_color = main_color
        self.accent_color = accent_color

        x0 = int(self.x_c * 0.1)
        x1 = int(self.x_c * 0.9)

        x = int(self.x_c // 2)

        y0 = int(self.y_c * 0.1)
        y1 = int(self.y_c * 0.9)

        l = len(self.choices)

        h = int(self.y_c * 0.8 // l)

        self.choices_boxes = list()


        for text, y in zip(self.choices.keys(), range(y0 + int(h // 2), y1, h)):
            font = pygame.font.SysFont("monospace", self.button_h)

            label = font.render(text, 1, main_color)

            rect = label.get_rect()
            rect.width = self.button_w
            self.height = self.button_h
            rect.center = x, y

            self.choices_boxes.append((label, rect, text) ,)


    def draw(self):
        for box in self.choices_boxes:
            pygame.draw.rect(self.screen, self.accent_color, pygame.Rect(box[1]))

            self.screen.blit(box[0], box[1])


    def check_buttons(self, x, y):
        for box in self.choices_boxes:
            rect = box[1]
            if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
                self.choices[box[2]]()

                self.running = False
                return None


    def make_choice(self, choices: dict):
        self.choices = choices
        self.generate()

        self.running = True
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = e.pos
                    self.check_buttons(x, y)

            self.screen.fill(self.main_color)
            self.draw()
            pygame.display.flip()

