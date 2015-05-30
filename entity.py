__author__ = 'anish'

from pyglet.window import key
from pyglet import image, sprite
from math import sin, cos, radians as r


class Entity:

    spritesheet = image.load("resources/sprites.png")


    def __init__(self, x, y, map):
        self.want_theta = -1
        self.theta = -1
        self.sunit = 1 / 16
        self.x = x
        self.y = y
        self.map = map
        self.gd = map.gd
        self.center = [self.x, self.y]
        self.pix_skip = 0

        self.can_right = self.can_left = self.can_up = self.can_down = False

    def update_movement_possibilities(self):

        self.can_right = self.map.grid[self.center[1].__int__()][self.center[0].__int__() + 1] != "b"
        self.can_left = self.map.grid[self.center[1].__int__()][self.center[0].__int__() - 1] != "b"
        self.can_up = self.map.grid[self.center[1].__int__() + 1][self.center[0].__int__()] != "b"
        self.can_down = self.map.grid[self.center[1].__int__() - 1][self.center[0].__int__()] != "b"

    def update(self):

        self.update_movement_possibilities()
        self.center = [self.x, self.y]

        if self.want_theta == -1:
            return None

        if self.want_theta == r(0) and self.can_right:
            self.theta = self.want_theta

        if self.want_theta == r(180) and self.can_left:
            self.theta = self.want_theta

        if self.want_theta == r(90) and self.can_up:
            self.theta = self.want_theta

        if self.want_theta == r(270) and self.can_down:
            self.theta = self.want_theta

        if self.theta == r(0) and self.can_right:
            self.x += self.sunit * cos(self.theta)

        if self.theta == r(180) and self.can_left:
            self.x += self.sunit * cos(self.theta)

        if self.theta == r(90) and self.can_up:
            self.y += self.sunit * sin(self.theta)

        if self.theta == r(270) and self.can_down:
            self.y += self.sunit * sin(self.theta)

    def calculate_center(self):
        self.center = [int(self.x), int(self.y)]

    def right(self):
        self.want_theta = r(0)

    def left(self):
        self.want_theta = r(180)

    def up(self):
        self.want_theta = r(90)

    def down(self):
        self.want_theta = r(270)


class Player(Entity):
    def __init__(self, cscheme, x, y, map):
        super().__init__(x, y, map)
        self.cscheme = cscheme
        self.keys = key.KeyStateHandler()
        self.sprites = []

        self.load_resources()

    def load_resources(self):

        spritesheet = Entity.spritesheet.get_region(0, Entity.spritesheet.height - 32, 32, 3 * 32)

        self.sprites = image.ImageGrid(spritesheet, 1, 3, item_width=32, item_height=32)
        for i in range(len(self.sprites)):
            self.sprites[i].anchor_x = self.sprites[i].width // 2
            self.sprites[i].anchor_y = self.sprites[i].width // 2

        self.sprites = [sprite.Sprite(i) for i in self.sprites]

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

        self.sprites[0].set_position(self.map.gd * self.x, self.map.gd * self.y)

    def draw(self):
        self.sprites[0].draw()


class Ghost(Entity):

    def __init__(self, x, y, map):
        super().__init__(x, y, map)