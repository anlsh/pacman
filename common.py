__author__ = 'anish'

# Just a file to contain constants and methods to be used throughout the project
from math import sin as s, cos as c, radians

# Number of times to update per second
CLOCKS_PER_SEC = 64
# Square width in the grid
GRID_DIM = 24

# sin of an angle in degrees since default sin is in radians
def sin(degrees):
    return s(radians(degrees))


# cos of an angle in degrees, since default cos is in radians
def cos(degrees):
    return c(radians(degrees))