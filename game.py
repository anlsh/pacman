from pyglet.window import key
from player import Player
from ghost import *
from common import *
from graphicsgroup import GraphicsGroup

from pyglet.gl import *
from ctypes import pointer, sizeof


class Game:

    def __init__(self, handle):
        '''
        This is... a really big class. It parses a grid from a game file, and takes care of drawing the grid, updating
        entities, etc.
        :param handle: The filename of the game to play
        :returns: Nothing
        '''

        # TODO implement procedural generation

        self.draw_rectangle = self.glVertex2f = self.draw_segment = self.draw_line = self.odraw_segment = None
        self.xoff = self.yoff = None
        self.graphics_group = GraphicsGroup(self, x=0, y=0)

        # Open a game file and convert it into a grid. Somewhat confusingly, the tile at (x,y) on the grid is accessed
        # by grid[y][x]. Up and right increase y and x respectively
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]

        # TODO Set spawn tiles for players and ghosts on the game
        self.players = [Player([key.W, key.A, key.S, key.D], 1.5, 1.5, self)]
        self.ghosts = [Blinky(1.5, 1.5, self), Pinky(1.5, 1.5, self), Inky(1.5, 1.5, self), Clyde(1.5, 1.5, self)]

        # Create a set of functions to loop through to draw a static game so a ton of constant conditionals aren't
        # checked on ever iteration
        self.line_points = []
        self.circle_points = []
        self.calculate_static_map()

        self.line_vbo = GLuint()
        glGenBuffers(1, pointer(self.line_vbo))
        self.line_points = (GLfloat*self.line_points.__len__())(*self.line_points)
        glBindBuffer(GL_ARRAY_BUFFER, self.line_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.line_points), 0, GL_STATIC_DRAW)

    def draw(self):

        # Draw the game, players, and ghosts
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_map()

        for p in self.players:
            p.draw()

        for g in self.ghosts:
            g.draw()

    def calculate_static_map(self):

        # A bit of premature optimization, but I'm proud of it. This method should only be run once per (static) game
        # instance. Instead of drawing the grid and having to check about a bazillion conditions which never change,
        # this checks all of them once and creates functions using functools.partial() to draw the game which can be
        # called quickly.
        # I'm not going to comment this method, that would take waaay too long. Maybe another day
        # TODO Comment this method

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

                        self.draw_line(x * GRID_DIM, y * GRID_DIM + GRID_DIM // 2, x * GRID_DIM + GRID_DIM,
                                        y * GRID_DIM + GRID_DIM // 2, self.line_points)

                    elif (empty_left or empty_right) and not empty_up and not empty_down:
                        self.draw_line(x * GRID_DIM + GRID_DIM // 2, y * GRID_DIM, x * GRID_DIM + GRID_DIM // 2,
                                                               y * GRID_DIM + GRID_DIM, self.line_points)

                    elif empty_up and empty_left and not empty_down and self.grid[y-1][x-1] != "b":
                        self.odraw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 90, 180,
                                           self.circle_points)

                    elif empty_up and empty_right and not empty_down and self.grid[y-1][x+1] != "b":
                        self.odraw_segment(x * GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 0, 90, self.circle_points)

                    elif empty_down and empty_left and not empty_up and self.grid[y+1][x-1] != "b":
                        self.odraw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180, 270,
                                           self.circle_points)

                    elif empty_down and empty_right and not empty_up and self.grid[y+1][x+1] != "b":
                        self.odraw_segment(x * GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 270, 360,
                                           self.circle_points)

                    try:
                        if self.grid[y-1][x-1] != "b" and not empty_left and not empty_down:
                            self.odraw_segment(x * GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 0, 90,
                                               self.circle_points)
                    except BaseException:
                        pass
                    try:
                        if self.grid[y-1][x+1] != "b" and not empty_right and not empty_down:
                            self.odraw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 90, 180,
                                               self.circle_points)
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x-1] != "b" and not empty_left and not empty_up:
                            self.odraw_segment(x * GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 270, 360,
                                               self.circle_points)
                    except BaseException:
                        pass
                    try:
                        if self.grid[y+1][x+1] != "b" and not empty_right and not empty_up:
                            self.odraw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180,
                                                270, self.circle_points)
                    except BaseException:
                        pass

    def draw_map(self):

        glColor3f(0, 0, 1)

        glBindBuffer(GL_ARRAY_BUFFER, self.line_vbo)
        glVertexPointer(2, GL_FLOAT, 0, 0)
        glDrawArrays(GL_POINTS, 0, 2)

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
