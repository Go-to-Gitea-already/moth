from pygame.sprite import Sprite, Group
from pygame.mask import from_surface
from pygame import Surface


class Base(Sprite):

    def __init__(self, coords: tuple, image: str, index: int, kind, next_base, radius: float,
                 sprites_group: Group):

        super().__init__(sprites_group)

        self.image = Surface((2 * radius, 2 * radius))
        self.mask = from_surface(self.image)
        self.rect = self.image.get_rect()

        self.generators = ['B']
        self.getters = ['A']

        self.coords = coords
        self.kind = kind
        self.next = next_base
        self.index = index
        self.radius = radius
        self.resource = 0

    def move(self, new_x: float, new_y: float):
        self.coords = (new_x, new_y)

    def update(self):
        if self.kind in self.generators:
            self.resource += 1

