__author__ = 'anish'
from map import Map

import pyglet
from pyglet.gl import *
from pyglet.window import key

class Driver(pyglet.window.Window):

    def __init__(self, width, length, gd):
        super().__init__(width, length)
        self.w = width
        self.l = length
        self.map = Map("map_classic.txt", gd)

    def update(self, dt):
        self.clear()
        self.push_handlers(self.map.keys)
        for x in self.map.players:
            self.push_handlers(x.keys)
        self.map.update()

    def draw(self, dt):
        self.clear()
        self.map.draw()

if __name__ == "__main__":
    gd = 24
    game = Driver(28*gd, 31*gd-32, gd)

    pyglet.clock.schedule_interval(game.update, 1/60)
    pyglet.clock.schedule(game.update)

    #pyglet.clock.schedule_interval(game.draw, 1/60)
    #pyglet.clock.schedule(game.draw)

    pyglet.app.run()