__author__ = 'anish'

from pyglet import image
from fractions import Fraction     # used to create accurate representations of position
from common import *


class Entity:

    # All entities load from the same spritesheet, so I just initialise it as a static variable
    spritesheet = image.load("resources/sprites.png")

    def __init__(self, x, y, game):

        self.x = Fraction(x)
        self.y = Fraction(y)

        self.game = game
        self.speed = Fraction(1, 20)
        self.theta = None

        self.can_right = self.can_left = self.can_up = self.can_down = False

    def update(self):
        '''
        Moves the play every iteration, also left unimplemented b/c ghosts and players move differently
        :return:
        '''
        if self.x <= 21/20 and self.theta == 180:
            self.x = Fraction(31 - self.speed, 1)
        if self.x >= 31 - self.speed and self.theta == 0:
            self.x = Fraction(1, 2)
