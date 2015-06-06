__author__ = 'anish'

import pyglet
import pyglet.font as fontlib
from pyglet.font import Text
from pyglet.gl import *
from common import *


class Menu:

    def __init__(self):

        fontlib.add_file("resources/prstartk.ttf")
        self.font = pyglet.font.load("Press Start K", 10, bold=True, italic=False)

        self.label = Text(self.font, "Pac-Man")

        self.menu_state = "main"