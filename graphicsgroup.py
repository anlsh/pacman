__author__ = 'anish'

from pyglet.gl import glBegin, glEnd, glLineWidth, glColor3f, glVertex2f, GL_QUADS, GL_LINE_LOOP, GL_LINE_STRIP, \
    GL_LINES
from common import *


class GraphicsGroup:

    # Class to draw stuff with offsets- it should also take care of ALL graphics related functions
    # The idea is to make it so that all graphics are abstracted away, and that if I port this to another language
    # then all graphics can be implemented by changing this file

    # glColor3f and glLineWidth, however, is fine and is left for use outside this class

    # DEPENDS PYGLET In case of port, this will need to be rewritten

    def __init__(self, map, x=0, y=0):

        self.xoff = x
        self.yoff = y

        map.xoff = x
        map.yoff = y

        glLineWidth(4)

        map.draw_rectangle = self.draw_rectangle
        map.glVertex2f = self.glVertex2f
        map.draw_segment = self.draw_segment
        map.draw_line = self.draw_line

    def draw_rectangle(self, x, y, w, h):

        glBegin(GL_QUADS)
        self.glVertex2f(x, y)
        self.glVertex2f(x+w, y)
        self.glVertex2f(x+w, y+h)
        self.glVertex2f(x, y+h)
        glEnd()

    def glVertex2f(self, x, y):

        glVertex2f(self.xoff + x, self.yoff + y)

    def draw_segment(self, x, y, radius, start_theta, stop_theta, step=10):

        glBegin(GL_LINE_STRIP)
        for i in range(step + 1):
            theta = start_theta + (stop_theta - start_theta) / step * i
            self.glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
        glEnd()

    def draw_line(self, x1, y1, x2, y2):

        glBegin(GL_LINES)
        self.glVertex2f(x1, y1)
        self.glVertex2f(x2, y2)
        glEnd()