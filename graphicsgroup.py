__author__ = 'anish'

from pyglet.gl import glBegin, glEnd, glLineWidth, glColor3f, glVertex2f, GL_QUADS, GL_LINE_LOOP, GL_LINE_STRIP, \
    GL_LINES
from functools import partial
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

        game.xoff = x
        game.yoff = y

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

        # TODO This method is much better than simply making calls to partial in drawing a static map, but FPS may
        # still dip to the high 40s intermittently even with a step of 1. Further optimizations are in order

        for i in range(step + 1):
            theta = start_theta + (stop_theta - start_theta) / step * i
            vertex_array.extend((x + radius * cos(theta), y + radius * sin(theta)))

    def old_odraw_segment(self, x, y, radius, start_theta, stop_theta, func_ptrs, step=2):
        # Optimised version of the draw_segment method, meant to push a set of function pointers onto
        # a pre-existing array

        # TODO This method is much better than simply making calls to partial in drawing a static map, but FPS may
        # still dip to the high 40s intermittently even with a step of 1. Further optimizations are in order

        func_ptrs.append(partial(glBegin, GL_LINE_STRIP))
        for i in range(step + 1):
            theta = start_theta + (stop_theta - start_theta) / step * i
            func_ptrs.append(partial(self.glVertex2f, x + radius * cos(theta), y + radius * sin(theta)))
        func_ptrs.append(partial(glEnd))

    def draw_line(self, x1, y1, x2, y2, vertex_array):

        vertex_array.extend((x1, y1, x2, y2))