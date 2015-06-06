__author__ = 'anish'
from game import Game
from menu import Menu

import pyglet
from pyglet.gl import *
import common as c


class Driver(pyglet.window.Window):

    def __init__(self, width, length, gd):
        super().__init__(width, length)
        self.w = width
        self.l = length
        self.game = Game("map_classic.txt")
        self.menu = Menu()

        self.state = "game"

        self.fps_display = pyglet.clock.ClockDisplay()

        # OpenGL config

        glLineWidth(4)
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnableClientState(GL_VERTEX_ARRAY)

    def update(self, dt):

        if self.state == "game":
            for x in self.game.players:
                self.push_handlers(x.keys)
            self.game.update()


    def on_draw(self):
        self.clear()
        self.game.draw()
        self.fps_display.draw()

if __name__ == "__main__":

    gd = c.GRID_DIM
    game = Driver(28*gd, 29*gd, gd)

    pyglet.clock.schedule_interval(game.update, 1 / c.CLOCKS_PER_SEC)
    pyglet.clock.set_fps_limit(60)

    pyglet.app.run()