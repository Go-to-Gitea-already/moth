import math

from engine import Engine

w = 1050
h = 1050

units_count = 154
unit_width = 2
unit_speed = 1
unit_hear_distance = 100

bases_count = 4
base_types = ['A', 'B']
base_radius = 30


master = Engine(w, h, units_count, bases_count, base_types, base_radius, unit_width, unit_speed, unit_hear_distance)

master.start()

