__author__ = 'anish'

from math import sin, cos, radians, pi
from pyglet.gl import *
CLOCKS_PER_SEC = 60
GRID_DIM = 24


def draw_arc(x, y, radius, start_theta=0, end_theta=360):
    glBegin(GL_LINE_LOOP)
    glColor3f(1.0, 1.0, 1.0)
    start_theta = radians(start_theta)
    end_theta = radians(end_theta)
    dtheta = (end_theta - start_theta / 10)
    while start_theta < end_theta:
        glVertex2i(int(x + radius * cos(start_theta)), int(y + radius * sin(start_theta)))
        start_theta += dtheta
    glEnd()