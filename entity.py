__author__ = 'anish'

from pyglet.window import key
from pyglet import image, sprite
from math import sin, cos, radians as r


class Entity:

    spritesheet = image.load("resources/sprites.png")

    def __init__(self, x, y, map):

        self.x = x
        self.y = y

        self.sunit = 1 / 22

        self.map = map
        self.gd = map.gd

        self.center = [self.x, self.y]

        self.can_right = self.can_left = self.can_up = self.can_down = False

    def update_movement_possibilities(self):

        raise NotImplementedError

    def update(self):

        raise NotImplementedError

    def calculate_center(self):
        self.center = [int(self.x), int(self.y)]


class Ghost(Entity):

    def __init__(self, x, y, map):
        super().__init__(x, y, map)