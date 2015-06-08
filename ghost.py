__author__ = 'anish'
from entity import Entity
from sprite import Sprite
from pyglet import image
from copy import copy
from common import *
from random import randint
from fractions import Fraction


class Ghost(Entity):

    def __init__(self, x, y, game):

        super().__init__(x, y, game)

        # setpoint coordinates
        self.start_x = x
        self.start_y = y
        self.escaped = False

        self.want_x = None
        self.want_y = None
        self.escape_tile = [15.5, 18.5]
        self.wanderpoint = []

        self.count = 0
        self.dot_threshold = None

        self.state = "idle"

        scared_spritesheet = Entity.spritesheet.get_region(4 * 32, 6 * 32, 4 * 32, 32)

        # Convert the image into an array of images, and center their anchor points <pyglet>
        self.scared_sprites = image.ImageGrid(scared_spritesheet, 1, 4, item_width=32, item_height=32)
        for i in range(len(self.scared_sprites)):
            self.scared_sprites[i].anchor_x = self.scared_sprites[i].width // 2
            self.scared_sprites[i].anchor_y = self.scared_sprites[i].width // 2

        # Convert the images in the array to sprites <pyglet>
        self.scared_sprites = [Sprite(i, self.game.graphics_group) for i in self.scared_sprites]

    def update_movement_possibilities(self):
        '''
        Method meant to calculate possible directions the entity can go in. This does not account for the no-reversal
        rule- that is taken care of in the update method. This simply tests for a block in the desired position
        :return: None
        '''
        #The .000001 is included to make sure that the method correctly detects the presence of a block on the game
        # The constant's value does not matter, but it should be smaller than 1 / self.speed
        self.can_up = self.x % 1 == 0.5 and self.game.grid[int(self.y + 0.5)][int(self.x)] != "b"
        self.can_left = self.y % 1 == 0.5 and self.game.grid[int(self.y)][int(self.x - 0.5 - .00000001)] != "b"
        self.can_down = self.x % 1 == 0.5 and self.game.grid[int(self.y - 0.5 - .000000001)][int(self.x)] != "b" and \
            self.game.grid[int(self.y - 0.5 - .000000001)][int(self.x)] != "g"
        self.can_right = self.y % 1 == 0.5 and self.game.grid[int(self.y)][int(self.x + 0.5)] != "b"

    def load_resources(self, row):
        '''
        :WARNING: This entire method is heavily dependent on pyglet-specific methods. It will need to be reworked if
        a port is attempted
        '''

        # Slice out the needed region of the sprite sheet (32 x 32 Pac-Man sprites) <pyglet>
        spritesheet = Entity.spritesheet.get_region(0, row * 32, 8 * 32, 32)

        # Convert the image into an array of images, and center their anchor points <pyglet>
        self.sprites = image.ImageGrid(spritesheet, 1, 8, item_width=32, item_height=32)
        for i in range(len(self.sprites)):
            self.sprites[i].anchor_x = self.sprites[i].width // 2
            self.sprites[i].anchor_y = self.sprites[i].width // 2

        # Convert the images in the array to sprites <pyglet>
        self.sprites = [Sprite(i, self.game.graphics_group) for i in self.sprites]

        temp = copy(self.sprites)
        self.sprites = {}
        angles = {90: temp[0], 270: temp[2], 180: temp[4], 0: temp[6]}
        self.sprites[0] = angles
        angles = {0: temp[7], 90: temp[1], 270: temp[3], 180: temp[5]}
        self.sprites[1] = angles

    def set_setpoint(self, x, y):
        '''
        :param x: x position of setpoint
        :param y: y position of setpoint
        :return: None
        '''
        self.want_x = x
        self.want_y = y

    def update(self):
        '''
        Moves the ghost towards the player
        :return: None
        '''

        super().update()

        if self.state == "chase":
            self.speed = Fraction(1, 20)
            self.x -= self.x % self.speed
            self.y -= self.y % self.speed
            if not self.escaped:
                self.state = "escape"
            self.set_setpoint(*self.target())
        if self.state == "wander":
            self.speed = Fraction(1, 20)
            self.x -= self.x % self.speed
            self.y -= self.y % self.speed
            if not self.escaped:
                self.state = "escape"
            self.set_setpoint(*self.wanderpoint)
        if self.state == "scared":
            self.speed = Fraction(1, 40)
            self.x -= self.x % self.speed
            self.y -= self.y % self.speed
            self.set_setpoint(*self.wander())
        if self.state == "flashing":
            self.speed = Fraction(1, 40)
            self.x -= self.x % self.speed
            self.y -= self.y % self.speed
            self.set_setpoint(*self.wander())
        if self.state == "idle":
            if self.game.dots_eaten >= self.dot_threshold:
                self.state = "escape"
                self.dot_threshold = 100000
            else:
                return None

        if self.state == "escape":
            self.speed = Fraction(1, 20)
            self.x -= self.x % self.speed
            self.y -= self.y % self.speed
            self.set_setpoint(*self.escape_tile)
            if [self.x, self.y] == self.escape_tile and not self.escaped:
                self.escaped = True
                self.state = "wander"

        if self.state == "retreat":
            self.speed = Fraction(1, 4)
            self.x -= self.x % self.speed
            self.y -= self.y % self.speed
            self.set_setpoint(*self.escape_tile)
            if [self.x, self.y] == self.escape_tile:
                self.state = "wander"

        self.low_level_update()

    def low_level_update(self):

        self.update_movement_possibilities()

        # The AI attempts to take the shortest path to target. The squares of the distances are actually used to avoid
        # having to call math.sqrt
        up_distance = pow(self.x - self.want_x, 2) + pow(self.y + self.speed - self.want_y, 2)
        left_distance = pow(self.x - self.speed - self.want_x, 2) + pow(self.y - self.want_y, 2)
        down_distance = pow(self.x - self.want_x, 2) + pow(self.y - self.speed - self.want_y, 2)
        right_distance = pow(self.x + self.speed - self.want_x, 2) + pow(self.y - self.want_y, 2)

        distances = [right_distance, left_distance, down_distance, up_distance]

        # This loop is needed to ensure that a valid theta is always set. If this is not included then sometimes an
        # appropriate theta will not be set because it is not the shortest path, allowing invalid paths to be taken

        theta_set = False

        while not theta_set:

            min_distance = min(distances)

            if self.can_up and up_distance == min_distance and self.theta != 270:
                self.theta = 90
                theta_set = True

            elif self.can_left and left_distance == min_distance and self.theta != 0:
                self.theta = 180
                theta_set = True

            elif self.can_down and down_distance == min_distance and self.theta != 90:
                self.theta = 270
                theta_set = True

            elif self.can_right and right_distance == min_distance and self.theta != 180:
                self.theta = 0
                theta_set = True

            #if none of the minimum distances are in valid directions, remove them from consideration and reloop
            for x in range(len(distances)):
                try:
                    distances.remove(min_distance)
                except ValueError:
                    break

        #update position
        self.x += self.speed * cos(self.theta).__int__()
        self.y += self.speed * sin(self.theta).__int__()

    def draw(self):
        '''
        Draw the appropriate sprite to the game
        :return: None
        '''
        self.count += .08

        #Based on the count and the current theta, draw a frame rotated at the appropriate angle

        try:
            if self.state != "scared" and self.state != "flashing":
                self.sprites[int(self.count % 2)][self.theta].set_position(int(self.x * GRID_DIM),
                                                                           int(self.y * GRID_DIM))
                self.sprites[int(self.count % 2)][self.theta].draw()

            elif self.state == "scared":
                self.scared_sprites[int(self.count % 2)].set_position(int(self.x * GRID_DIM),
                                                                           int(self.y * GRID_DIM))
                self.scared_sprites[int(self.count % 2)].draw()

            elif self.state == "flashing":
                self.scared_sprites[int(self.count % 4)].set_position(int(self.x * GRID_DIM),
                                                                           int(self.y * GRID_DIM))
                self.scared_sprites[int(self.count % 4)].draw()

        except KeyError:
            self.sprites[int(self.count % 2)][90].set_position(self.x * GRID_DIM, self.y * GRID_DIM)
            self.sprites[int(self.count % 2)][90].draw()

    def wander(self):

        return [randint(0, 32), randint(0, 31)]


class Blinky(Ghost):

    def __init__(self, x, y, game):

        super().__init__(x, y, game)
        self.load_resources(5)
        self.wanderpoint = [57/2, 61/2]
        self.dot_threshold = 0

    def target(self):
        return [self.game.players[0].x, self.game.players[0].y]


class Pinky(Ghost):

    def __init__(self, x, y, game):

        super().__init__(x, y, game)
        self.load_resources(4)
        self.wanderpoint = [7/2, 61/2]
        self.dot_threshold = 30

    def target(self):

        return [self.game.players[0].x + 4 * cos(self.game.players[0].theta),
                              self.game.players[0].y + 4 * sin(self.game.players[0].theta)]


class Inky(Ghost):

    def __init__(self, x, y, game):

        super().__init__(x, y, game)
        self.load_resources(3)
        self.wanderpoint = [7/2, 1/2]
        self.dot_threshold = 60

    def target(self):
        x1 = self.game.players[0].x + 2 * cos(self.game.players[0].theta)
        y1 = self.game.players[0].y + 2 * sin(self.game.players[0].theta)

        vecx = x1 - self.game.ghosts[0].x
        vecy = y1 - self.game.ghosts[0].y

        return [self.game.ghosts[0].x + 2 * vecx, self.game.ghosts[0].y + 2 * vecy]


class Clyde(Ghost):

    def __init__(self, x, y, game):

        super().__init__(x, y, game)
        self.load_resources(2)
        self.wanderpoint = [57/2, 1/2]
        self.dot_threshold = 90

    def target(self):
        if pow(self.x - self.game.players[0].x, 2) + pow(self.y - self.game.players[0].y, 2) <= 64:
                return [30, -1]
        else:
            return [self.game.players[0].x, self.game.players[0].y]