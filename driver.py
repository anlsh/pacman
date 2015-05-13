__author__ = 'anish'
from grid import Map

import pyglet
from pyglet.gl import *

'''
throwaway driver for inconsequential tasks
'''
sx = 28*16
sy = 31*16 - 32
window = pyglet.window.Window(sx, sy)

map = Map("map_classic.txt")

@window.event
def on_draw():
    for y in range(len(map.grid)):
        for x in range(len(map.grid[y]))[::-1]:
            u = map.grid[y][x]
            if u.id == "b":
                glColor3f(0, 0, 1)
            elif u.id == "e" or u.id == "d":
                glColor3f(0, 0, 0)
            elif u.id == "w":
                glColor3f(1, 0, 1)
            elif u.id == "p":
                glColor3f(1, 1, 0)

            glBegin(GL_QUADS)
            glVertex2i(x*16, y*16)
            glVertex2i(x*16+16, y*16)
            glVertex2i(x*16+16, y*16+16)
            glVertex2i(x*16, y*16+16)
            glEnd()

if __name__ == "__main__":
    pyglet.app.run()