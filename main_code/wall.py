class Wall:

    def __init__(self, first_point: tuple, second_point: tuple, width: int, kind):
        self.first_point = first_point
        self.second_point = second_point
        self.width = width
        self.kind = kind
        self.length = ((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2) ** 0.5
