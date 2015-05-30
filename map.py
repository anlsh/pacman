from pyglet.window import key
from pyglet.gl import *
from pyglet.gl.gl import glVertex2i
from player import Player
from math import radians as r
from Common import *
from functools import partial

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

        self.players = [Player([key.W, key.A, key.S, key.D], 1.5, 1.5, self)]

        self.map_draw_functions = []
        self.calculate_static_map()

    def draw(self):
        self.draw_map()
        for p in self.players:
            p.draw()

    def draw_rect(self, x, y, w, h):
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        glBegin(GL_QUADS)
        self.glVertex2i(x, y)
        self.glVertex2i(x+w, y)
        self.glVertex2i(x+w, y+h)
        self.glVertex2i(x, y+h)
        glEnd()

    def glVertex2i(self, x, y):
        glVertex2i(int(self.xoff + x), int(self.yoff + y))

    def calculate_static_map(self):

        self.map_draw_functions.append(partial(glColor3f, 0, 0, 1))
        self.map_draw_functions.append(partial(glLineWidth, 4))
        for y in range(len(self.grid)):

            for x in range(len(self.grid[y]))[::-1]:

                u = self.grid[y][x]

                if u == "b":

                    try:
                        empty_up = self.grid[y+1][x] != "b"
                    except BaseException:
                        empty_up = False
                    try:
                        empty_down = self.grid[y-1][x] != "b"
                    except BaseException:
                        empty_down = False
                    try:
                        empty_right = self.grid[y][x+1] != "b"
                    except BaseException:
                        empty_right = False
                    try:
                        empty_left = self.grid[y][x-1] != "b"
                    except BaseException:
                        empty_left = False

                    if (empty_up or empty_down) and not empty_left and not empty_right:
                        #glBegin(GL_LINES)
                        self.map_draw_functions.append(partial(glBegin, GL_LINES))
                        #glVertex2i(x * self.gd, y * self.gd + self.gd // 2)
                        self.map_draw_functions.append(partial(glVertex2i, x * self.gd, y * self.gd + self.gd // 2))
                        #glVertex2i(x * self.gd + self.gd, y * self.gd + self.gd // 2)
                        self.map_draw_functions.append(partial(glVertex2i, x * self.gd + self.gd,
                                                               y * self.gd + self.gd // 2))
                        #glEnd()
                        self.map_draw_functions.append(partial(glEnd))

                    elif (empty_left or empty_right) and not empty_up and not empty_down:
                        #glBegin(GL_LINES)
                        self.map_draw_functions.append(partial(glBegin, GL_LINES))
                        #glVertex2i(x * self.gd + self.gd // 2, y * self.gd)
                        self.map_draw_functions.append(partial(glVertex2i, x * self.gd + self.gd // 2, y * self.gd))
                        #glVertex2i(x * self.gd + self.gd // 2, y * self.gd + self.gd)
                        self.map_draw_functions.append(partial(glVertex2i, x * self.gd + self.gd // 2, y * self.gd + self.gd))
                        #glEnd()
                        self.map_draw_functions.append(partial(glEnd))

                    elif empty_up and empty_left and not empty_down and self.grid[y-1][x-1] != "b":
                        #draw_segment(x * self.gd + self.gd, y * self.gd, self.gd // 2, 90, 180)
                        self.map_draw_functions.append(partial(draw_segment, x * self.gd + self.gd, y * self.gd, self.gd // 2, 90, 180))

                    elif empty_up and empty_right and not empty_down and self.grid[y-1][x+1] != "b":
                        #draw_segment(x * self.gd, y * self.gd, self.gd // 2, 0, 90)
                        self.map_draw_functions.append(partial(draw_segment, x * self.gd, y * self.gd, self.gd // 2, 0, 90))

                    elif empty_down and empty_left and not empty_up and self.grid[y+1][x-1] != "b":
                        #draw_segment(x * self.gd + self.gd, y * self.gd + self.gd, self.gd // 2, 180, 270)
                        self.map_draw_functions.append(partial(draw_segment, x * self.gd + self.gd, y * self.gd + self.gd, self.gd // 2, 180, 270))

                    elif empty_down and empty_right and not empty_up and self.grid[y+1][x+1] != "b":
                        #draw_segment(x * self.gd, y * self.gd + self.gd, self.gd // 2, 270, 360)
                        self.map_draw_functions.append(partial(draw_segment, x * self.gd, y * self.gd + self.gd, self.gd // 2, 270, 360))

                    try:
                        if self.grid[y-1][x-1] != "b" and not empty_left and not empty_down:
                            #draw_segment(x * self.gd, y * self.gd, self.gd // 2, 0, 90)
                            self.map_draw_functions.append(partial(draw_segment, x * self.gd, y * self.gd, self.gd // 2,
                                                                   0, 90))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y-1][x+1] != "b" and not empty_right and not empty_down:
                            #draw_segment(x * self.gd + self.gd, y * self.gd, self.gd // 2, 90, 180)
                            self.map_draw_functions.append(partial(draw_segment, x * self.gd + self.gd, y * self.gd,
                                                                   self.gd // 2, 90, 180))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x-1] != "b" and not empty_left and not empty_up:
                            #draw_segment(x * self.gd, y * self.gd + self.gd, self.gd // 2, 270, 360)
                            self.map_draw_functions.append(partial(draw_segment, x * self.gd, y * self.gd + self.gd,
                                                                   self.gd // 2, 270, 360))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x+1] != "b" and not empty_right and not empty_up:
                            #draw_segment(x * self.gd + self.gd, y * self.gd + self.gd, self.gd // 2, 180, 270)
                            self.map_draw_functions.append(partial(draw_segment, x * self.gd + self.gd, y * self.gd +
                                                                   self.gd, self.gd // 2, 180, 270))
                    except BaseException:
                        pass

    def draw_map(self):

        for f in self.map_draw_functions:
            f()

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y]))[::-1]:

                u = self.grid[y][x]
                pass

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
