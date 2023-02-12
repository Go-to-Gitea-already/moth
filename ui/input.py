import pygame as pygame


pygame.init()
COLOR_INACTIVE = (200, 100, 0)
COLOR_ACTIVE = (255, 128, 0)
FONT = pygame.font.Font(None, 32)


class InputBox:

    def __init__(self, engine, x, y, w, h, text=''):
        self.rect = pygame.Rect(0, 0, 0, 0)
        print(x, y, w, h)
        self.rect.top = y
        self.rect.left = x
        self.rect.width = w
        self.rect.height = h

        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.engine = engine
        self.screen = engine.screen
        self.is_main = False


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if self.active and event.key == pygame.K_RETURN:
                    return self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)


    def draw(self):
        self.screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(self.screen, self.color, self.rect, 2)


    def update(self):
        # width = max(200, self.txt_surface.get_width()+10)
        # self.rect.w = width

        self.draw()

        for event in (self.events if self.is_main else self.engine.events):
            out = self.handle_event(event)
            if out is not None:
                return out

        return None

    
    def wait(self):
        out = None

        self.is_main = True

        while out is None:
            self.screen.fill((0, 0, 0))

            self.events = pygame.event.get()

            out = self.update()

            pygame.display.flip()

        self.is_main = False

        return out


