__author__ = 'anish'

from math import sin, cos, radians, pi
from pyglet.gl import *
CLOCKS_PER_SEC = 64
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


#http://slabode.exofire.net/circle_draw.shtml
def draw_circle(cx, cy, r, num_segments):
    theta = 2 * pi / num_segments
    c = cos(theta)
    s = sin(theta)

    x = r
    y = 0

    glBegin(GL_LINE_LOOP)
    for ii in range(num_segments):
        glVertex2f(x + cx, y + cy)

        t = x
        x = c * x - s * y
        y = s * t + c * y
    glEnd()


def draw_semicircle(cx, cy, r, mode, num_segments=20):
    theta = 2 * pi / num_segments
    c = cos(theta)
    s = sin(theta)

    if mode == "up":
        x = r
        y = 0
    elif mode == "down":
        x = -r
        y = 0
    elif mode == "left":
        x = 0
        y = r
    elif mode == "right":
        x = 0
        y = -r

    glBegin(GL_LINE_LOOP)
    for ii in range(num_segments // 4 + 1):
        glVertex2f(x + cx, y + cy)

        t = x
        x = c * x - s * y
        y = s * t + c * y

    glEnd()


def draw_segment(x, y, radius, start_theta, stop_theta, step=10):
    start_theta = radians(start_theta)
    stop_theta = radians(stop_theta)
    glBegin(GL_LINE_STRIP)
    for i in range(step + 1):
        theta = start_theta + (stop_theta - start_theta) / step * i
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()