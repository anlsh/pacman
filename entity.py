__author__ = 'anish'

from pyglet.window import key
from math import sin, cos, radians as r


class Entity:

    def __init__(self, x, y, map, gd):
        self.want_theta = -1
        self.theta = -1
        self.sunit = 1
        self.x = x
        self.y = y
        self.map = map
        self.gd = gd

        self.block_right = self.block_left = self.block_up = self.block_down = False

    def update_movement_possibilities(self):

        self.block_right = self.map[int(self.y / self.gd)][int((self.x + self.gd) / self.gd)] == "b" or \
            self.map[int((self.y + self.gd - 1) / self.gd)][int((self.x + self.gd) / self.gd)] == "b"
        self.block_left = self.map[int(self.y / self.gd)][int((self.x - 1) / self.gd)] == "b" or \
            self.map[int((self.y + self.gd - 1) / self.gd)][int((self.x - 1) / self.gd)] == "b"

        self.block_up = self.map[int((self.y + self.gd) / self.gd)][int(self.x / self.gd)] == "b" or \
            self.map[int((self.y + self.gd) / self.gd)][int((self.x + self.gd - 1) / self.gd)] == "b"
        self.block_down = self.map[int((self.y - 1) / self.gd)][int(self.x / self.gd)] == "b" or \
            self.map[int((self.y - 1) / self.gd)][int((self.x + self.gd - 1) / self.gd)] == "b"

    def update(self):

        self.update_movement_possibilities()

        if self.want_theta == -1:
            return None

        if self.want_theta == r(0) and not self.block_right:
            self.theta = self.want_theta

        if self.want_theta == r(180) and not self.block_left:
            self.theta = self.want_theta

        if self.want_theta == r(90) and not self.block_up:
            self.theta = self.want_theta

        if self.want_theta == r(270) and not self.block_down:
            self.theta = self.want_theta

        if self.theta == r(0) and not self.block_right:
            self.x += self.sunit * cos(self.theta)

        if self.theta == r(180) and not self.block_left:
            self.x += self.sunit * cos(self.theta)

        if self.theta == r(90) and not self.block_up:
            self.y += self.sunit * sin(self.theta)

        if self.theta == r(270) and not self.block_down:
            self.y += self.sunit * sin(self.theta)

    def right(self):
        self.want_theta = r(0)

    def left(self):
        self.want_theta = r(180)

    def up(self):
        self.want_theta = r(90)

    def down(self):
        self.dy = self.want_theta = r(270)


class Player(Entity):
    def __init__(self, cscheme, x, y, map, gd):
        super().__init__(x, y, map, gd)
        self.cscheme = cscheme
        self.keys = key.KeyStateHandler()

    def update(self):

        if self.keys[self.cscheme[0]]:
            self.up()
        if self.keys[self.cscheme[1]]:
            self.left()
        if self.keys[self.cscheme[2]]:
            self.down()
        if self.keys[self.cscheme[3]]:
            self.right()

        Entity.update(self)