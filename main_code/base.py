class Base:

    def __init__(self, coords: dict, kind, next_base, index: int, radius: float):
        self.coords = coords
        self.kind = kind
        self.next = next_base
        self.index = index
        self.radius = radius


