__author__ = 'anish'

from pyglet import image
from fractions import Fraction     # used to create accurate representations of position
from common import *


class Entity:

    # All entities load from the same spritesheet, so I just initialise it as a static variable
    spritesheet = image.load("resources/sprites.png")
    map_dims = None
    padding = None

    def __init__(self, game, x, y):

        self.x = Fraction(x)
        self.y = Fraction(y)

        self.game = game
        self.base_speed = Fraction(1, 20)
        self.speed = self.base_speed
        self.speed_factor = Fraction(1, 1)
        self.theta = None

        self.can_right = self.can_left = self.can_up = self.can_down = False

    def update_movement_possibilities(self):
        '''
        Convenience method for the update method, left unimplemented b/c ghosts and players behave differently
        :returns: Nothing
        '''
        raise NotImplementedError

    def update(self):

        if self.x <= Fraction(1, 2) and self.theta == 180:
            self.x = Fraction(Entity.map_dims[1] + Fraction(Entity.padding[0]) - Fraction(1, 2))

        elif self.x >= Fraction(Entity.map_dims[1] + Fraction(Entity.padding[0]) - Fraction(1, 2)) and self.theta == 0:
            self.x = Fraction(1, 2)