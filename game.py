from pyglet.window import key
from player import Player
from ghost import *
from common import *
from governor import *
from graphicsgroup import GraphicsGroup

import pyglet
import pyglet.font as fontlib

from pyglet.gl import *
from ctypes import pointer, sizeof
import time


class Game:

    def __init__(self, window, handle="map_classic.txt", xoff=0, yoff=0):
        '''
        This is... a really big class. It parses a grid from a game file, and takes care of drawing the grid, updating
        entities, etc.
        :param handle: The filename of the game to play
        :returns: Nothing
        '''

        self.over = False
        fontlib.add_file("resources/prstartk.ttf")
        self.font = fontlib.load("Press Start K", 10, bold=True, italic=False)

        self.draw_rectangle = self.glVertex2f = self.draw_segment = self.draw_line = self.odraw_segment = None
        self.xoff = xoff
        self.yoff = yoff
        self.graphics_group = GraphicsGroup(self, x=xoff, y=yoff)

        # Open a game file and convert it into a grid. Somewhat confusingly, the tile at (x,y) on the grid is accessed
        # by grid[y][x]. Up and right increase y and x respectively
        self.handle = handle
        self.init_map()

        self.players = self.ghosts = None

        self.init_buffers()

        self.level = 1
        self.score = 0
        self.lives = 3
        self.dots_eaten = 0
        self.pups_eaten = 0
        self.governor = Governor(self)

        self.score_label = pyglet.text.Label("foo",
                          font_name='Press Start K',
                          font_size=12,
                          x=0, y=0)

        self.lives_label = pyglet.text.Label("foo",
                          font_name='Press Start K',
                          font_size=12,
                          x=0, y=20)

    def init_map(self):
        with open(self.handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]

    def init_buffers(self):

        # Create a set of functions to loop through to draw a static game so a ton of constant conditionals aren't
        # checked on ever iteration
        self.line_points = []
        self.circle_points = []
        self.circle_chunks = []
        self.calculate_static_map()

        # Set up buffers and upload relevant vertex data to them, this is muy faster than using glBegin, etc...

        self.line_points = self.graphics_group.transform_array(self.line_points)
        self.line_data_l = self.line_points.__len__()
        self.line_vbo = GLuint()
        glGenBuffers(1, pointer(self.line_vbo))
        self.line_gldata = (GLfloat*self.line_data_l)(*self.line_points)
        glBindBuffer(GL_ARRAY_BUFFER, self.line_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.line_gldata), pointer(self.line_gldata), GL_STATIC_DRAW)

        # Circles require some special treatment

        self.circle_points = self.graphics_group.transform_array(self.circle_points)
        self.circle_data_l = self.circle_points.__len__()
        self.chunks = [self.circle_points[x:x+2] for x in range(0, len(self.circle_points), 2)]
        self.circle_vbos = copy(self.chunks)

        self.circle_vbo = GLuint()
        glGenBuffers(1, pointer(self.circle_vbo))
        self.circle_gldata = (GLfloat*self.circle_data_l)(*self.circle_points)
        glBindBuffer(GL_ARRAY_BUFFER, self.circle_vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(self.circle_gldata), pointer(self.circle_gldata), GL_STATIC_DRAW)

    def draw(self):

        # Draw the game, players, and ghosts
        self.draw_map()

        for p in self.players:
            p.draw()

        for g in self.ghosts:
            g.draw()

        self.score_label.draw()
        self.lives_label.draw()

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

    def update(self):

        if self.dots_eaten == 236:
            #reset the map
            self.level += 1
            self.init_map()
            self.governor = Governor(self)
            self.dots_eaten = 0
            self.pups_eaten = 0
            time.sleep(3)

        self.governor.update()

        for p in self.players:
            p.update()
            if self.grid[int(p.y)][int(p.x)] == "d":
                self.dots_eaten += 1
                self.score += 10
                self.grid[int(p.y)][int(p.x)] = "e"

            elif self.grid[int(p.y)][int(p.x)] == "p":
                self.pups_eaten += 1
                self.score += 50
                self.grid[int(p.y)][int(p.x)] = "e"
                self.governor.fire_pup()

        for g in self.ghosts:
            g.set_setpoint(self.players[0].x, self.players[0].y)
            g.update()

            if [int(g.x), int(g.y)] == [int(self.players[0].x), int(self.players[0].y)]:
                if g.state == "scared" or g.state == "retreat" or g.state == "flashing":
                    self.score += 200
                    g.state = "retreat"

                else:
                    self.lives -= 1

                    if self.lives > 0:
                        time.sleep(3)
                        self.governor = Governor(self)

                    else:
                        time.sleep(3)
                        self.over = True

        self.lives_label.text = "Lives:" + str(self.lives)
        self.score_label.text = "Score:" + str(self.score)