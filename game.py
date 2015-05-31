from pyglet.window import key
from pyglet.gl import glColor3f
from player import Player
from ghost import *
from common import *
from functools import partial
from graphicsgroup import GraphicsGroup


class Game:

    def __init__(self, handle):
        '''
        This is... a really big class. It parses a grid from a game file, and takes care of drawing the grid, updating
        entities, etc.
        :param handle: The filename of the game to play
        :returns: Nothing
        '''

        # TODO implement procedural generation

        self.draw_rectangle = self.glVertex2f = self.draw_segment = self.draw_line = None
        self.xoff = self.yoff = None
        self.graphics_group = GraphicsGroup(self, x=0, y=0)

        # Open a game file and convert it into a grid. Somewhat confusingly, the tile at (x,y) on the grid is accessed
        # by grid[y][x]. Up and right increase y and x respectively
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]
        
        # Populate the game
        # TODO Set spawn tiles for players and ghosts on the game
        self.players = [Player([key.W, key.A, key.S, key.D], 1.5, 1.5, self)]
        self.ghosts = [Blinky(1.5, 1.5, self), Pinky(1.5, 1.5, self), Inky(1.5, 1.5, self), Clyde(1.5, 1.5, self)]

        # Create a set of functions to loop through to draw a static game so a ton of constant conditionals aren't
        # checked on ever iteration
        self.map_draw_functions = []
        self.calculate_static_map()

        # Score!
        self.score = 0

    def draw(self):

        # Draw the game, players, and ghosts
        self.draw_map()

        for p in self.players:
            p.draw()

        for g in self.ghosts:
            g.draw()

        glColor3f(1, 0, 0)

    def calculate_static_map(self):

        # A bit of premature optimization, but I'm proud of it. This method should only be run once per (static) game
        # instance. Instead of drawing the grid and having to check about a bazillion conditions which never change,
        # this checks all of them once and creates functions using functools.partial() to draw the game which can be
        # called quickly.
        # I'm not going to comment this method, that would take waaay too long. Maybe another day
        # TODO Comment this method

        self.map_draw_functions.append(partial(glColor3f, 0, 0, 1))

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

                        self.map_draw_functions.append(partial(self.draw_line, x * GRID_DIM,
                                                               y * GRID_DIM + GRID_DIM // 2, x * GRID_DIM + GRID_DIM,
                                                               y * GRID_DIM + GRID_DIM // 2))

                    elif (empty_left or empty_right) and not empty_up and not empty_down:
                        self.map_draw_functions.append(partial(self.draw_line, x * GRID_DIM + GRID_DIM // 2,
                                                               y * GRID_DIM, x * GRID_DIM + GRID_DIM // 2,
                                                               y * GRID_DIM + GRID_DIM))

                    elif empty_up and empty_left and not empty_down and self.grid[y-1][x-1] != "b":
                        self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM + GRID_DIM, y * GRID_DIM,
                                                               GRID_DIM // 2, 90, 180))

                    elif empty_up and empty_right and not empty_down and self.grid[y-1][x+1] != "b":
                        self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM,
                                                               y * GRID_DIM, GRID_DIM // 2, 0, 90))

                    elif empty_down and empty_left and not empty_up and self.grid[y+1][x-1] != "b":
                        self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM + GRID_DIM,
                                                               y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180, 270))

                    elif empty_down and empty_right and not empty_up and self.grid[y+1][x+1] != "b":
                        self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM, y * GRID_DIM + GRID_DIM,
                                                                GRID_DIM // 2, 270, 360))

                    try:
                        if self.grid[y-1][x-1] != "b" and not empty_left and not empty_down:
                            self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM, y * GRID_DIM,
                                                            GRID_DIM // 2, 0, 90))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y-1][x+1] != "b" and not empty_right and not empty_down:
                            self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM + GRID_DIM,
                                                                   y * GRID_DIM, GRID_DIM // 2, 90, 180))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x-1] != "b" and not empty_left and not empty_up:
                            self.map_draw_functions.append(partial(self. draw_segment, x * GRID_DIM,
                                                                   y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 270, 360))
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x+1] != "b" and not empty_right and not empty_up:
                            self.map_draw_functions.append(partial(self.draw_segment, x * GRID_DIM + GRID_DIM,
                                                                   y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180, 270))
                    except BaseException:
                        pass

    def draw_map(self):

        #Draw the static game
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
