import math

from engine import Engine

w = 400
h = 400

units_count = 200
unit_width = 2
unit_speed = 1
unit_hear_distance = 25

bases_count = 4
base_types = ['A', 'B']
base_radius = 30


master = Engine(w, h, units_count, bases_count, base_types, base_radius, unit_width, unit_speed, unit_hear_distance)

master.start()

