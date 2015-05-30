__author__ = 'anish'

from math import sin, cos, radians, pi
from pyglet.gl import *
CLOCKS_PER_SEC = 64
GRID_DIM = 24


#http://slabode.exofire.net/circle_draw.shtml
def draw_segment(x, y, radius, start_theta, stop_theta, step=10):
    start_theta = radians(start_theta)
    stop_theta = radians(stop_theta)
    glBegin(GL_LINE_STRIP)
    for i in range(step + 1):
        theta = start_theta + (stop_theta - start_theta) / step * i
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()