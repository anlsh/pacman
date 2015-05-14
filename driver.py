__author__ = 'anish'
from grid import Grid

import pyglet
from pyglet.gl import *
from pyglet.window import key

'''
throwaway driver for inconsequential tasks
'''
sx = 28*16
sy = 31*16 - 32
window = pyglet.window.Window(sx, sy)

map = Grid("map_classic.txt")
py = 1
px = 1
@window.event
def on_key_press(symbol, mods):
    global px
    global py
    if symbol == key.A:
        px = 1
        py = 1
    if symbol == key.UP:
        py += 1
    if symbol == key.RIGHT:
        px += 1
    if symbol == key.DOWN:
        py -= 1
    if symbol == key.LEFT:
        px -= 1

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

    global px
    global py
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex2i(px*16, py*16)
    glVertex2i(px*16+16, py*16)
    glVertex2i(px*16+16, py*16+16)
    glVertex2i(px*16, py*16+16)
    glEnd()

if __name__ == "__main__":
    pyglet.app.run()