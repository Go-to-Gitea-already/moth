from pygame.sprite import Sprite, Group
from pygame.mask import from_surface
from pygame.image import load
from os.path import join as os_join


class Base(Sprite):
    def __init__(self, coords=(0, 0), image="./data/default_base.jpg", index=0, kind=0, next_base=1, radius=15,
                 sprites_group=Group(), dict_converted=None):

        super().__init__(sprites_group)

        self.generators = ['B']
        self.getters = ['A']

        self.coords = coords
        self.kind = kind
        self.next = next_base
        self.index = index
        self.radius = radius
        self.resource = 0

        if dict_converted is not None:
            for key, value in dict_converted.items():
                setattr(self, key, value)


    def move(self, new_x: float, new_y: float):
        self.coords = (new_x, new_y)

    def update(self):
        if self.kind in self.generators:
            self.resource += 1

