__author__ = 'anish'
from map import Map

import pyglet
from pyglet.gl import *
from pyglet.window import key
import Common as c


class Driver(pyglet.window.Window):

    def __init__(self, width, length, gd):
        super().__init__(width, length)
        self.w = width
        self.l = length
        self.map = Map("map_classic.txt", gd)

    def update(self, dt):

        self.push_handlers(self.map.keys)
        for x in self.map.players:
            self.push_handlers(x.keys)
        self.map.update()

    def on_draw(self):
        self.clear()
        self.map.draw()

if __name__ == "__main__":
    gd = c.GRID_DIM
    game = Driver(28*gd, 29*gd, gd)

    pyglet.clock.schedule_interval(game.update, 1 / c.CLOCKS_PER_SEC)
    pyglet.clock.schedule(game.update)

    pyglet.clock.set_fps_limit(60)

    pyglet.app.run()