from pygame.sprite import Sprite, Group
from pygame.mask import from_surface
from pygame.image import load
from os.path import join as os_join


class Base(Sprite):

    def __init__(self, coords: tuple[float, float], image: str, index: int, kind, next_base, radius: float,
                 sprites_group: Group):

        self.image = load(os_join('data', image))

        self.mask = from_surface(self.image)

        super().__init__(sprites_group)

        self.coords = coords
        self.kind = kind
        self.next = next_base
        self.index = index
        self.radius = radius

    def move(self, new_x: float, new_y: float):
        self.coords = (new_x, new_y)

    def update(self):
        pass
