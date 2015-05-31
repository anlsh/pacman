__author__ = 'anish'
from entity import Entity
from sprite import Sprite
from pyglet import image
from copy import copy
from common import *


class Ghost(Entity):

    # TODO make the class use sprites

    def __init__(self, x, y, game, want_x=None, want_y=None):

        super().__init__(x, y, game)

        # setpoint coordinates
        self.want_x = None
        self.want_y = None

        self.count = 0

        self.state = "wander"

        if want_x is None or want_y is None:
            self.set_setpoint(x, y)
        else:
            self.set_setpoint(want_x, want_y)

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
        # TODO Implement targeting for multiple players if I have time

        self.update_movement_possibilities()

        # The AI attempts to take the shortest path to target. The squares of the distances are actually used to avoid
        # having to call math.sqrt
        up_distance = pow(self.x - self.want_x, 2) + pow(self.y + self.speed - self.want_y, 2)
        left_distance = pow(self.x - self.speed - self.want_x, 2) + pow(self.y - self.want_y, 2)
        down_distance = pow(self.x - self.want_x, 2) + pow(self.y - self.speed - self.want_y, 2)
        right_distance = pow(self.x + self.speed - self.want_x, 2) + pow(self.y - self.want_y, 2)

        distances = [right_distance, left_distance, down_distance, up_distance]

        if self.x != self.want_x or self.y != self.want_y:

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
        # TODO Right now this just draws a box, I need to make it draw sprites
        self.count += .08

        #Based on the count and the current theta, draw a frame rotated at the appropriate angle

        try:
            self.sprites[int(self.count % 2)][self.theta].set_position(int(self.x * GRID_DIM), int(self.y * GRID_DIM))
            self.sprites[int(self.count % 2)][self.theta].draw()
        except KeyError:
            self.sprites[0][0].set_position(self.x * GRID_DIM, self.y * GRID_DIM)
            self.sprites[0][0].draw()


class Blinky(Ghost):

    def __init__(self, x, y, game, want_x=None, want_y=None):

        super().__init__(x, y, game, want_x, want_y)
        self.load_resources(5)

    def update(self):

        if self.state == "chase":
            self.set_setpoint(self.game.players[0].x, self.game.players[0].y)
        elif self.state == "wander":
            self.set_setpoint(100, 100)
        elif self.state == "scared":
            # TODO implement a common "run" method for ghosts to use when scared
            pass

        super().update()


class Pinky(Ghost):

    def __init__(self, x, y, game, want_x=None, want_y=None):

        super().__init__(x, y, game, want_x, want_y)
        self.load_resources(4)

    def update(self):

        if self.state == "chase":
            self.set_setpoint(self.game.players[0].x + 4 * cos(self.game.players[0].theta),
                              self.game.players[0].y + 4 * sin(self.game.players[0].theta))
        elif self.state == "wander":
            self.set_setpoint(0, 100)
        elif self.state == "scared":
            # TODO implement a common "run" method for ghosts to use when scared
            pass

        super().update()


class Inky(Ghost):

    def __init__(self, x, y, game, want_x=None, want_y=None):

        super().__init__(x, y, game, want_x, want_y)
        self.load_resources(3)

    def update(self):

        if self.state == "chase":
            x1 = self.game.players[0].x + 2 * cos(self.game.players[0].theta)
            y1 = self.game.players[0].y + 2 * sin(self.game.players[0].theta)

            vecx = x1 - self.game.ghosts[0].x
            vecy = y1 - self.game.ghosts[0].y

            self.set_setpoint(self.game.ghosts[0].x + 2 * vecx, self.game.ghosts[0].y + 2 * vecy)

        elif self.state == "wander":
            self.set_setpoint(0, -5)
        elif self.state == "scared":
            # TODO implement a common "run" method for ghosts to use when scared
            pass

        super().update()


class Clyde(Ghost):

    def __init__(self, x, y, game, want_x=None, want_y=None):

        super().__init__(x, y, game, want_x, want_y)
        self.load_resources(2)

    def update(self):

        if self.state == "chase":
            if pow(self.x - self.game.players[0].x, 2) + pow(self.y - self.game.players[0].y, 2) <= 64:
                self.set_setpoint(30, -1)
            else:
                self.set_setpoint(self.game.players[0].x, self.game.players[0].y)

        elif self.state == "wander":
            self.set_setpoint(30, -1)
        elif self.state == "scared":
            # TODO implement a common "run" method for ghosts to use when scared
            pass

        super().update()