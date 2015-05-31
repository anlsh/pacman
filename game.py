from pyglet.window import key
from pyglet.gl import *
from pyglet.gl.gl import glVertex2i
from player import Player
from ghost import Ghost
from math import radians as r
from common import *
from functools import partial
from fractions import Fraction


class Game:

    def __init__(self, handle):
        '''
        This is... a really big class. It parses a grid from a map file, and takes care of drawing the grid, updating
        entities, etc.
        :param handle: The filename of the map to play
        :returns: Nothing
        '''

        # TODO implement procedural generation

        # Open a map file and convert it into a grid. Somewhat confusingly, the tile at (x,y) on the grid is accessed
        # by grid[y][x]. Up and right increase y and x respectively
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]

        # Create a set of functions to loop through to draw a static map so a ton of constant conditionals aren't
        # checked on ever iteration
        self.map_draw_functions = []
        self.calculate_static_map()
        
        # Populate the map
        # TODO Set spawn tiles for players and ghosts on the map
        self.players = [Player([key.W, key.A, key.S, key.D], 1.5, 1.5, self)]
        self.ghosts = [Ghost(1.5, 1.5, self)]

        # Gives an offset to draw everything, needed to draw the game in a larger window. Non-functional right now
        # TODO Implement a Game.glVertex2i method which everything the game contains imports to draw with an offset
        self.xoff = self.yoff = 0

        # Score!
        self.score = 0

    def draw(self):

        # Draw the map, players, and ghosts
        self.draw_map()

        for p in self.players:
            p.draw()

        for g in self.ghosts:
            g.draw()

        glColor3f(1, 0, 0)

    def draw_rect(self, x, y, w, h):

        # I dont think I actually used this anymore, it's only left in for testing purposes
        # The purpose is simple though. The thing draws a rectangle

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

        # I was talking about making this earlier, looks like I already have one
        # TODO Make other functions use this method ('s offset) to draw
        glVertex2i(int(self.xoff + x), int(self.yoff + y))

    def calculate_static_map(self):

        # A bit of premature optimization, but I'm proud of it. This method should only be run once per (static) map
        # instance. Instead of drawing the grid and having to check about a bazillion conditions which never change,
        # this checks all of them once and creates functions using functools.partial() to draw the map which can be
        # called quickly.
        # I'm not going to comment this method, that would take waaay too long. Maybe another day
        # TODO Comment this method

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
                        #glVertex2i(x * GRID_DIM, y * GRID_DIM + GRID_DIM // 2)
                        self.map_draw_functions.append(partial(self.glVertex2i,
                                                               x * GRID_DIM, y * GRID_DIM + GRID_DIM // 2))
                        #glVertex2i(x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM // 2)
                        self.map_draw_functions.append(partial(self.glVertex2i, x * GRID_DIM + GRID_DIM,
                                                               y * GRID_DIM + GRID_DIM // 2))
                        #glEnd()
                        self.map_draw_functions.append(partial(glEnd))

                    elif (empty_left or empty_right) and not empty_up and not empty_down:
                        #glBegin(GL_LINES)
                        self.map_draw_functions.append(partial(glBegin, GL_LINES))
                        #glVertex2i(x * GRID_DIM + GRID_DIM // 2, y * GRID_DIM)
                        self.map_draw_functions.append(partial(self.glVertex2i,
                                                               x * GRID_DIM + GRID_DIM // 2, y * GRID_DIM))
                        #glVertex2i(x * GRID_DIM + GRID_DIM // 2, y * GRID_DIM + GRID_DIM)
                        self.map_draw_functions.append(partial(self.glVertex2i,
                                                               x * GRID_DIM + GRID_DIM // 2, y * GRID_DIM + GRID_DIM))
                        #glEnd()
                        self.map_draw_functions.append(partial(glEnd))

                    elif empty_up and empty_left and not empty_down and self.grid[y-1][x-1] != "b":
                        #draw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 90, 180)
                        self.map_draw_functions.append(partial(draw_segment,
                                                               x * GRID_DIM + GRID_DIM, y * GRID_DIM,
                                                               GRID_DIM // 2, 90, 180))

                    elif empty_up and empty_right and not empty_down and self.grid[y-1][x+1] != "b":
                        #draw_segment(x * GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 0, 90)
                        self.map_draw_functions.append(partial(draw_segment,
                                                               x * GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 0, 90))

                    elif empty_down and empty_left and not empty_up and self.grid[y+1][x-1] != "b":
                        #draw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180, 270)
                        self.map_draw_functions.append(partial(draw_segment,
                                                               x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM,
                                                               GRID_DIM // 2, 180, 270))

                    elif empty_down and empty_right and not empty_up and self.grid[y+1][x+1] != "b":
                        #draw_segment(x * GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 270, 360)
                        self.map_draw_functions.append(partial(draw_segment,
                                                               x * GRID_DIM, y * GRID_DIM + GRID_DIM,
                                                               GRID_DIM // 2, 270, 360))

                    try:
                        if self.grid[y-1][x-1] != "b" and not empty_left and not empty_down:
                            #draw_segment(x * GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 0, 90)
                            self.map_draw_functions.append(partial(draw_segment, x * GRID_DIM, y * GRID_DIM, GRID_DIM // 2,
                                                                   0, 90))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y-1][x+1] != "b" and not empty_right and not empty_down:
                            #draw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 90, 180)
                            self.map_draw_functions.append(partial(draw_segment, x * GRID_DIM + GRID_DIM, y * GRID_DIM,
                                                                   GRID_DIM // 2, 90, 180))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x-1] != "b" and not empty_left and not empty_up:
                            #draw_segment(x * GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 270, 360)
                            self.map_draw_functions.append(partial(draw_segment, x * GRID_DIM, y * GRID_DIM + GRID_DIM,
                                                                   GRID_DIM // 2, 270, 360))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x+1] != "b" and not empty_right and not empty_up:
                            #draw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180, 270)
                            self.map_draw_functions.append(partial(draw_segment, x * GRID_DIM + GRID_DIM, y * GRID_DIM +
                                                                   GRID_DIM, GRID_DIM // 2, 180, 270))
                    except BaseException:
                        pass

    def draw_map(self):

        #Draw the static map
        for f in self.map_draw_functions:
            f()

        # In this method dynamic things (like dots) should be drawn, but it's not implemented right now
        # TODO Implement drawing dots

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y]))[::-1]:

                u = self.grid[y][x]

    def update(self):

        # Update players and ghosts
        # TODO Make a Governor class which will direct the behaviour (mode) of the ghosts
        # TODO Implement eating dots
        for p in self.players:
            p.update()

        for g in self.ghosts:
            g.set_setpoint(self.players[0].x, self.players[0].y)
            g.update()

    def eat(self, y, x):

        # Method to eat dots, not used anywhere
        # TODO Use this method somewhere
        self.grid[y][x] = "e"
        self.score += 1
