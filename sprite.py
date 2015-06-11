__author__ = 'anish'

from pyglet.sprite import Sprite as SuperSprite
from common import *


class Sprite(SuperSprite):

    # Abstraction for pyglet's sprite class
    # DEPENDS Pyglet

    def __init__(self, image, graphicsgroup):

        super().__init__(image)

        self.xoff = graphicsgroup.xoff
        self.yoff = graphicsgroup.yoff

        self.scale = GRID_DIM / 24

    def set_position(self, x, y):
        super().set_position(self.xoff + int(x), self.yoff + int(y))

    def set_rotation(self, theta):
        self.rotation = -theta