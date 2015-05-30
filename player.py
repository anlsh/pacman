__author__ = 'anish'

from entity import *
from pyglet.window import key
from math import sin, cos, radians as r


class Player(Entity):

    def __init__(self, cscheme, x, y, map):
        super().__init__(x, y, map)
        self.cscheme = cscheme
        self.keys = key.KeyStateHandler()
        self.sprites = []
        self.theta = -1
        self.want_theta = -1
        self.last_theta = -1
        self.horizontal_mismatch = False
        self.vertical_mismatch = False

        self.sunit = Fraction(1, 20)

        self.load_resources()

    def load_resources(self):

        spritesheet = Entity.spritesheet.get_region(0, Entity.spritesheet.height - 32, 32, 3 * 32)

        self.sprites = image.ImageGrid(spritesheet, 1, 3, item_width=32, item_height=32)
        for i in range(len(self.sprites)):
            self.sprites[i].anchor_x = self.sprites[i].width // 2
            self.sprites[i].anchor_y = self.sprites[i].width // 2

        self.sprites = [sprite.Sprite(i) for i in self.sprites]
        for s in self.sprites:
            s.set_position(self.gd * self.x, self.gd * self.y)

    def update_movement_possibilities(self):
        self.can_right = True \
            if self.map.grid[int(self.y)][int(self.x) + 1] != "b" else self.x % 1 < 0.5
        self.can_left = True \
            if self.map.grid[int(self.y)][int(self.x) - 1] != "b" else self.x % 1 > 0.5
        self.can_up = True \
            if self.map.grid[int(self.y) + 1][int(self.x)] != "b" else self.y % 1 < 0.5
        self.can_down = True \
            if self.map.grid[int(self.y) - 1][int(self.x)] != "b" else self.y % 1 > 0.5

    def update(self):

        if self.keys[self.cscheme[0]]:
            self.want_theta = r(90)
        if self.keys[self.cscheme[1]]:
            self.want_theta = r(180)
        if self.keys[self.cscheme[2]]:
            self.want_theta = r(270)
        if self.keys[self.cscheme[3]]:
            self.want_theta = r(0)

        self.update_movement_possibilities()
        temp_theta = self.theta

        if self.want_theta == -1:
            return None

        if self.want_theta == r(0) and self.can_right:
            if (self.map.grid[int(self.y)][int((self.x + self.sunit)) + 1] != "b") \
                and ((self.theta == r(90) and self.y % 1 <= 0.5) or
                (self.theta == r(270) and self.y % 1 >= 0.5) or
                self.theta == r(180) or self.theta == -1):
                    self.theta = self.want_theta

        if self.want_theta == r(180) and self.can_left:
            if (self.map.grid[int(self.y)][int((self.x - self.sunit)) - 1] != "b") \
                and ((self.theta == r(90) and self.y % 1 <= 0.5) or
                (self.theta == r(270) and self.y % 1 >= 0.5) or
                self.theta == r(0) or self.theta == -1):
                    self.theta = self.want_theta

        if self.want_theta == r(90) and self.can_up:
            if (self.map.grid[int((self.y + self.sunit)) + 1][int(self.x)] != "b") \
                and ((self.theta == r(0) and self.x % 1 <= 0.5) or
                (self.theta == r(180) and self.x % 1 >= 0.5) or
                self.theta == r(270) or self.theta == -1):
                    self.theta = self.want_theta

        if self.want_theta == r(270) and self.can_down:
            if (self.map.grid[int((self.y - self.sunit)) - 1][int(self.x)] != "b") \
                and ((self.theta == r(0) and self.x % 1 <= 0.5) or
                (self.theta == r(180) and self.x % 1 >= 0.5) or
                self.theta == r(90) or self.theta == -1):
                    self.theta = self.want_theta

        if self.theta == r(0) and self.can_right:
            self.x += self.sunit * cos(self.theta).__int__()

        if self.theta == r(180) and self.can_left:
            self.x += self.sunit * cos(self.theta).__int__()

        if self.theta == r(90) and self.can_up:
            self.y += self.sunit * sin(self.theta).__int__()

        if self.theta == r(270) and self.can_down:
            self.y += self.sunit * sin(self.theta).__int__()

        if temp_theta != self.theta:
            self.last_theta = temp_theta

        self.horizontal_mismatch = (self.theta == r(90) or self.theta == r(270)) \
                                        and (self.last_theta == r(0) or self.last_theta == r(180))

        self.vertical_mismatch = (self.theta == r(0) or self.theta == r(180)) \
                                        and (self.last_theta == r(90) or self.last_theta == r(270))

        if self.horizontal_mismatch:
            if self.x % 1 != 0.5:
                self.x += self.sunit * cos(self.last_theta).__int__()
            else:
                self.horizontal_mismatch = False

        if self.vertical_mismatch:
            if self.y % 1 != 0.5:
                self.y += self.sunit * sin(self.last_theta).__int__()
            else:
                self.vertical_mismatch = False

        self.sprites[0].set_position(self.map.gd * self.x, self.map.gd * self.y)

    def draw(self):
        self.sprites[0].draw()

