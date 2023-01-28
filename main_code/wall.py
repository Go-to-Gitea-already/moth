from pygame.sprite import Sprite, Group
from pygame.mask import from_surface
from pygame.image import load
from os.path import join as os_join


class Wall(Sprite):

    def __init__(self, first_point: tuple[float, float], second_point: tuple[float, float], kind: int,
                 sprites_group: Group, width: int):

        self.length = ((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2) ** 0.5

        super().__init__(sprites_group)

        self.first_point = first_point
        self.second_point = second_point
        self.width = width
        self.kind = kind
