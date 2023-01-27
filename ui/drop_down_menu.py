from ui.buttons import Buttons
import pygame


class DropDownMenu(Buttons):
    def __init__(self, engine, choices: dict, x=0, y=0, button_h=10, button_w=10, **kvargs):
        if kvargs.get('rect') is None:
            rect = pygame.Rect((0, 0), (0, 0))

            height = len(choices.keys()) * button_h * 1.9
            width = button_w

            rect.left = x + button_w
            rect.y = y - height // 2

            rect.height = height
            rect.width = width

#             kvargs['rect'] = rect

        super().__init__(engine, choices, rect=rect, button_h=button_h, button_w=button_w, **kvargs)

