__author__ = 'anish'

from pyglet.gl import glLineWidth, glVertex2f, GL_QUADS
from common import *


class GraphicsGroup:

    # Class to draw stuff with offsets- it should also take care of ALL graphics related functions
    # The idea is to make it so that all graphics are abstracted away, and that if I port this to another language
    # then all graphics can be implemented by changing this file

    # glColor3f and glLineWidth, however, is fine and is left for use outside this class

    # DEPENDS PYGLET In case of port, this will need to be rewritten

    def __init__(self, game, x=0, y=0):

        self.xoff = x
        self.yoff = y

        game.draw_rectangle = self.draw_rectangle
        game.glVertex2f = self.glVertex2f
        game.draw_segment = self.draw_segment
        game.draw_line = self.draw_line
        game.odraw_segment = self.odraw_segment

    def draw_rectangle(self, x, y, w, h):

        glBegin(GL_QUADS)
        self.glVertex2f(x, y)
        self.glVertex2f(x+w, y)
        self.glVertex2f(x+w, y+h)
        self.glVertex2f(x, y+h)
        glEnd()

    def glVertex2f(self, x, y):

        glVertex2f(self.xoff + x, self.yoff + y)

    def draw_segment(self, x, y, radius, start_theta, stop_theta, step=2):

        # This method is a ridiculously massive bottleneck, single-handedly causing the FPS to periodically drop by
        # 10-20. Because of that, I'm leaving it undone right now

        glBegin(GL_LINE_STRIP)
        for i in range(step + 1):
            theta = start_theta + (stop_theta - start_theta) / step * i
            self.glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
        glEnd()

    def odraw_segment(self, x, y, radius, start_theta, stop_theta, vertex_array, step=2):

        # Even more optimisations on the draw_segment method- this adds relevant vertexes to a vertex array

        for i in range(step + 1):
            theta = start_theta + (stop_theta - start_theta) / step * i
            vertex_array.extend((self.xoff + x + radius * cos(theta), self.yoff + y + radius * sin(theta)))
            if i != 0 and i != step:
                vertex_array.extend((self.xoff + x + radius * cos(theta), self.yoff + y + radius * sin(theta)))

    def draw_line(self, x1, y1, x2, y2, vertex_array):

        vertex_array.extend((x1, y1, x2, y2))

    def transform_array(self, arr):

        for i in range(len(arr)):
            if i % 2 == 0:
                arr[i] += self.xoff
            else:
                arr[i] += self.yoff

        return arr