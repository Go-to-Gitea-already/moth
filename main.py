import math

from engine import Engine

w = 900
h = 900

units_count = 221
unit_width = 6
unit_speed = 3
unit_hear_distance = 45

bases_count = 4
base_types = ['A', 'B']
base_radius = 45


master = Engine(w, h, units_count, bases_count, base_types, base_radius, unit_width, unit_speed, unit_hear_distance)

master.start()

