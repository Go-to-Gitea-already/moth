import pygame


class Label:
    def __init__(self, engine, text="", rect=None):
        self.text = text

        if rect is None:
            self.rect = pygame.Rect(0, 0, *engine.screen.get_size())
        else:
            self.rect = rect

        self.engine = engine


    def draw(self, color=(255, 128, 0), font="monospace", font_size=12, gap=12):
        strings = self.text.split("\n")
        font = pygame.font.SysFont(font, font_size)

        for m, s in zip(range(0, 12 * len(strings), 12), strings):
            text = font.render(s, True, color)
            rect = text.get_rect()
            rect.center = (self.rect.center[0], rect.y + m + font_size)

            self.engine.screen.blit(text, rect)

