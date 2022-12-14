import math

from engine import Engine

w = 700
h = 700

units_count = 600
unit_width = 2
unit_speed = 1
unit_hear_distance = 50

bases_count = 4
base_types = ['A', 'B', 'C', 'D']
base_radius = 30


master = Engine(w, h, units_count, bases_count, base_types, base_radius, unit_width, unit_speed, unit_hear_distance)

master.start()

