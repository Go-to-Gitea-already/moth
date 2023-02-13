from pygame.sprite import Sprite, Group
from pygame.mask import from_surface
from pygame.image import load
from os.path import join as os_join


class Wall(Sprite):
    def __init__(self, first_point=[0.0, 0.0], second_point=[1.0, 1.0], kind=0,
                 sprites_group=Group(), width=5, dict_converted=None):

        self.length = ((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2) ** 0.5

        super().__init__(sprites_group)

        self.first_point = first_point
        self.second_point = second_point
        self.width = width
        self.kind = kind

        if dict_converted is not None:
            for key, value in dict_converted.items():
                setattr(self, key, value)

