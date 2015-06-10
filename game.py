from pyglet.window import key
from player import Player
from ghosts import *
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

        self.xoff = 0
        self.yoff = 0
        self.graphics_group = GraphicsGroup(self, x=self.xoff, y=self.yoff)

        self.dots_eaten = self.pups_eaten = 0

        # Open a game file and convert it into a grid. Somewhat confusingly, the tile at (x,y) on the grid is accessed
        # by grid[y][x]. Up and right increase y and x respectively
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]

        # TODO Set spawn tiles for players and ghosts on the game
        self.players = [Player([key.W, key.A, key.S, key.D], 1.5, 1.5, self)]
        self.ghosts = [Blinky(1.5, 1.5, self), Pinky(1.5, 1.5, self), Inky(1.5, 1.5, self), Clyde(1.5, 1.5, self)]

        self.init_buffers()

    def update(self):

        # Update players and ghosts
        # TODO Make a Governor class which will direct the behaviour (mode) of the ghosts

        for p in self.players:
            p.update()

            if self.grid[int(p.y)][int(p.x)] == "d":

                self.grid[int(p.y)][int(p.x)] = "e"
                self.dots_eaten += 1

        for g in self.ghosts:
            g.update()

    def draw(self):

        # Draw the game, players, and ghosts
        self.draw_map()

        for p in self.players:
            p.draw()

        for g in self.ghosts:
            g.draw()

    def draw_map(self):

        glColor3f(0, 0, 1)

        # Draw lines
        glBindBuffer(GL_ARRAY_BUFFER, self.line_vbo)
        glVertexPointer(2, GL_FLOAT, 0, 0)
        glDrawArrays(GL_LINES, 0, self.line_data_l)

        # Draw circles
        glBindBuffer(GL_ARRAY_BUFFER, self.circle_vbo)
        glVertexPointer(2, GL_FLOAT, 0, 0)
        glDrawArrays(GL_LINES, 0, self.circle_data_l)

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y])):

                if self.grid[y][x] == "d":
                    glColor3f(1, 1, 0)
                    glPointSize(5 / 24 * GRID_DIM)
                    glBegin(GL_POINTS)
                    self.glVertex2f(GRID_DIM * x + GRID_DIM / 2, GRID_DIM * y + GRID_DIM / 2)
                    glEnd()

                elif self.grid[y][x] == "p":
                    glColor3f(1, 20/255, 147/255)
                    glPointSize(7 / 24 * GRID_DIM)
                    glBegin(GL_POINTS)
                    self.glVertex2f(GRID_DIM * x + GRID_DIM / 2, GRID_DIM * y + GRID_DIM / 2)
                    glEnd()

    def calculate_static_map(self):

        # A bit of premature optimization, but I'm proud of it. This method should only be run once per (static) game
        # instance. Instead of drawing the grid and having to check about a bazillion conditions which never change,
        # this checks all of them once and creates functions using functools.partial() to draw the game which can be
        # called quickly.
        # I'm not going to comment this method, that would take waaay too long. Maybe another day

        for y in range(len(self.grid)):

            for x in range(len(self.grid[y]))[::-1]:

                u = self.grid[y][x]

                if u == "b":

                    try:
                        empty_up = self.grid[y+1][x] != "b"
                    except IndexError:
                        empty_up = False
                    try:
                        empty_down = self.grid[y-1][x] != "b"
                    except IndexError:
                        empty_down = False
                    try:
                        empty_right = self.grid[y][x+1] != "b"
                    except IndexError:
                        empty_right = False
                    try:
                        empty_left = self.grid[y][x-1] != "b"
                    except IndexError:
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
                    except IndexError:
                        pass
                    try:
                        if self.grid[y-1][x+1] != "b" and not empty_right and not empty_down:
                            self.odraw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM, GRID_DIM // 2, 90, 180,
                                               self.circle_points)
                    except IndexError:
                        pass
                    try:
                        if self.grid[y+1][x-1] != "b" and not empty_left and not empty_up:
                            self.odraw_segment(x * GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 270, 360,
                                               self.circle_points)
                    except IndexError:
                        pass
                    try:
                        if self.grid[y+1][x+1] != "b" and not empty_right and not empty_up:
                            self.odraw_segment(x * GRID_DIM + GRID_DIM, y * GRID_DIM + GRID_DIM, GRID_DIM // 2, 180,
                                                270, self.circle_points)
                    except IndexError:
                        pass

    def init_buffers(self):

        # Create a set of functions to loop through to draw a static game so a ton of constant conditionals aren't
        # checked on ever iteration
        self.line_points = []
        self.circle_points = []
        self.calculate_static_map()

        # Set up buffers and upload relevant vertex data to them, this is muy faster than using glBegin, etc...

        self.line_data_l = self.line_points.__len__()
        self.line_vbo = GLuint()
        glGenBuffers(1, pointer(self.line_vbo))
        self.line_gldata = (GLfloat*self.line_data_l)(*self.line_points)
        glBindBuffer(GL_ARRAY_BUFFER, self.line_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.line_gldata), pointer(self.line_gldata), GL_STATIC_DRAW)

        self.circle_data_l = self.circle_points.__len__()
        self.circle_vbo = GLuint()
        glGenBuffers(1, pointer(self.circle_vbo))
        self.circle_gldata = (GLfloat*self.circle_data_l)(*self.circle_points)
        glBindBuffer(GL_ARRAY_BUFFER, self.circle_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.circle_gldata), pointer(self.circle_gldata), GL_STATIC_DRAW)
