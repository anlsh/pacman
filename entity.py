__author__ = 'anish'

from pyglet import image, sprite   # although sprite is not used, it is imported here for all entites
from fractions import Fraction     # used to create accurate representations of position
from common import *


class Entity:

    # All entities load from the same spritesheet, so I just initialise it as a static variable
    spritesheet = image.load("resources/sprites.png")

    def __init__(self, x, y, map):

        self.x = Fraction(x)
        self.y = Fraction(y)

        self.map = map
        self.speed = Fraction(1, 20)
        self.theta = None

        self.can_right = self.can_left = self.can_up = self.can_down = False

    def update_movement_possibilities(self):
        '''
        Convenience method for the update method, left unimplemented b/c ghosts and players behave differently
        :returns: Nothing
        '''
        raise NotImplementedError

    def update(self):
        '''
        Moves the play every iteration, also left unimplemented b/c ghosts and players move differently
        :return:
        '''
        raise NotImplementedError