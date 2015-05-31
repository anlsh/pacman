__author__ = 'anish'

# Just a file to contain constants and methods to be used throughout the project
from math import sin as s, cos as c, radians
from pyglet.gl import *

# Number of times to update per second
CLOCKS_PER_SEC = 64
# Square width in the grid
GRID_DIM = 24


# http://slabode.exofire.net/circle_draw.shtml
# The above is an efficient way to draw circles. However I didnt really understand it, or how I could modify it to draw
# partial circles, so I just used the simply + inefficient way of doing it
# TODO Make this more efficient using the advice given above

def draw_segment(x, y, radius, start_theta, stop_theta, step=10):
    glBegin(GL_LINE_STRIP)
    for i in range(step + 1):
        theta = start_theta + (stop_theta - start_theta) / step * i
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()


# sin of an angle in degrees since default sin is in radians
def sin(degrees):
    return s(radians(degrees))


# cos of an angle in degrees, since default cos is in radians
def cos(degrees):
    return c(radians(degrees))