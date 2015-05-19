from pyglet import image, sprite
from pyglet.gl import *
from pyglet.gl.gl import glVertex2i


class Map:
    '''
    Simple class to read a map from a text file and parse it
    '''
    def __init__(self, handle):
    #Pacman map is 28 by 31 just by url http://upload.wikimedia.org/wikipedia/en/5/59/Pac-man.png
        self.gd = 16
        self.lw = 2
        self.dd = 4
        self.pd = 6
        self.xoff = self.yoff = 0
    
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]
            
    def draw(self):
        self.draw_map()

    def draw_rect(self, x, y, w, h):
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        self.glVertex2i(x, y)
        self.glVertex2i(x+w, y)
        self.glVertex2i(x+w, y+h)
        self.glVertex2i(x, y+h)

    def glVertex2i(self, x, y):
        glVertex2i(self.xoff + x, self.yoff + y)
        
    def draw_map(self):

        glBegin(GL_QUADS)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y]))[::-1]:
                u = self.grid[y][x]

                if u == "b":
                    glColor3f(0, 0, 1)
                    '''
                    self.glVertex2i(x*self.gd, y*self.gd)
                    self.glVertex2i((x+1)*self.gd, y*self.gd)
                    self.glVertex2i((x+1)*self.gd, (y+1)*self.gd)
                    self.glVertex2i(x*self.gd, (y+1)*self.gd)
                    '''
                    #glColor3f(0, .5, .75)

                    right = True
                    try:
                        right = (self.grid[y][x+1] != "b")
                    except IndexError:
                        pass

                    if right:
                        self.draw_rect((x+1)*self.gd, y*self.gd, -self.lw, self.gd)

                    up = True
                    try:
                        up = self.grid[y+1][x] != "b"
                    except IndexError:
                        pass

                    if up:
                        self.draw_rect(x*self.gd, (y+1)*self.gd, self.gd, -self.lw)

                    down = True
                    try:
                        down = self.grid[y-1][x] != "b"
                    except IndexError:
                        pass

                    #I dont want bordering on the next two, the others give a nice shading effect
                    #down = False
                    if down:
                        self.draw_rect(x*self.gd, y*self.gd, self.gd, self.lw)

                    left = True
                    try:
                        left = self.grid[y][x-1] != "b"
                    except IndexError:
                        pass

                    #left = False

                    if left:
                        self.draw_rect(x*self.gd, y*self.gd, self.lw, self.gd)

                elif u == "e":
                    glColor3f(0, 0, 0)
                    self.draw_rect(x*self.gd, y*self.gd, self.gd, self.gd)

                elif u == "d":
                    glColor3f(0, 0, 0)
                    self.draw_rect(x*self.gd, y*self.gd, self.gd, self.gd)
                    glColor3f(.5, .5, 0)
                    self.draw_rect(x*self.gd + ((self.gd-self.dd)/2), y*self.gd + ((self.gd-self.dd)/2),
                                   self.dd, self.dd)

                elif u == "w":
                    glColor3f(0, 0, 0)
                    self.draw_rect(x*self.gd, y*self.gd, self.gd, self.gd)

                elif u == "p":
                    glColor3f(0, 0, 0)
                    self.draw_rect(x*self.gd, y*self.gd, self.gd, self.gd)
                    glColor3f(255.0/255, 105.0/255, 180.0/255)
                    self.draw_rect(x*self.gd + ((self.gd-self.pd)/2), y*self.gd + ((self.gd-self.pd)/2),
                                   self.pd, self.pd)

        glEnd()