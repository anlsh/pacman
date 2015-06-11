__author__ = 'anish'
from game import Game

import pyglet
from pyglet.gl import *
from common import *


class Driver(pyglet.window.Window):

    def __init__(self, width, length, number_players=1):

        self.number_players = number_players

        super().__init__(width, length)
        self.w = width
        self.l = length

        self.key_states = pyglet.window.key.KeyStateHandler()

        self.game = Game("classic.map", wanted_players=self.number_players, xoff=0, yoff=100)

        self.pre_add = True
        self.pre_pause = True

        glLineWidth(4)
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnableClientState(GL_VERTEX_ARRAY)

    def update(self, dt):

        self.push_handlers(self.key_states)

        if self.key_states[pyglet.window.key.K] and not self.pre_add:
            if self.number_players < self.game.governor.map_max_players
                self.game = Game("classic.map", wanted_players=self.number_players, xoff=0, yoff=100)

        if self.key_states[pyglet.window.key.O] and not self.pre_pause:
            self.game.should_update = not self.game.should_update

        if not self.game.over:
            for x in self.game.players:
                self.push_handlers(x.keys)

            self.game.update()

        else:
            self.game = Game("classic.map", wanted_players=self.number_players, xoff=0, yoff=100)

        self.pre_add = self.key_states[pyglet.window.key.K]
        self.pre_pause = self.key_states[pyglet.window.key.O]

    def on_draw(self):
        self.clear()
        self.game.draw()

if __name__ == "__main__":

    game = Driver(28 * GRID_DIM, 29 * GRID_DIM + 100)

    pyglet.clock.schedule_interval(game.update, 1 / CLOCKS_PER_SEC)
    pyglet.clock.set_fps_limit(60)

    pyglet.app.run()