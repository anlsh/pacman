from pyglet.window import key
from pyglet.gl import *
from pyglet.gl.gl import glVertex2i
from entity import Player
from math import radians as r
import Common as c


class Map:

    def __init__(self, handle, gd):
    #Pacman map is 28 by 31 just by url http://upload.wikimedia.org/wikipedia/en/5/59/Pac-man.png
        self.gd = gd
        self.lw = 2
        self.dd = 4
        self.pd = 6
        self.score = 0
        self.xoff = self.yoff = 0
        self.keys = key.KeyStateHandler()
    
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]

        self.players = [Player([key.W, key.A, key.S, key.D], 1, 1, self)]

    def draw(self):
        glBegin(GL_QUADS)
        self.draw_map()
        glEnd()
        for p in self.players:
            p.draw()

    def draw_rect(self, x, y, w, h):
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        self.glVertex2i(x, y)
        self.glVertex2i(x+w, y)
        self.glVertex2i(x+w, y+h)
        self.glVertex2i(x, y+h)

    def glVertex2i(self, x, y):
        glVertex2i(int(self.xoff + x), int(self.yoff + y))

    def draw_map(self):

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y]))[::-1]:
                u = self.grid[y][x]

    def update(self):

        for p in self.players:
            p.update()

            if p.theta == r(0) or p.theta == r(90):
                if self.grid[int((p.y + self.gd / 4) / self.gd)][int((p.x + self.gd / 4) / self.gd)] == "d":
                    self.eat(int((p.y + self.gd / 4) / self.gd), int((p.x + self.gd / 4) / self.gd))
            else:
                if self.grid[int((p.y + self.gd / 2) / self.gd)][int((p.x + self.gd / 2) / self.gd)] == "d":
                    self.eat(int((p.y + self.gd / 2) / self.gd), int((p.x + self.gd / 2) / self.gd))

    def eat(self, y, x):
        self.grid[y][x] = "e"
        self.score += 1
