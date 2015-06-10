__author__ = 'anish'

from ghost import *


class Blinky(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(5)
        #TODO This is hardcoded, fix
        self.wanderpoint = [100, 100]
        self.dot_threshold = 2

    def target(self):
        return [self.game.players[0].x, self.game.players[0].y]


class Pinky(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(4)
        #TODO This is hardcoded, fix
        self.wanderpoint = [7/2, 61/2]
        self.dot_threshold = 30

    def target(self):

        return [self.game.players[0].x + 4 * cos(self.game.players[0].theta),
                              self.game.players[0].y + 4 * sin(self.game.players[0].theta)]


class Inky(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(3)
        #TODO This is hardcoded, fix
        self.wanderpoint = [7/2, 1/2]
        self.dot_threshold = 60

    def target(self):
        x1 = self.game.players[0].x + 2 * cos(self.game.players[0].theta)
        y1 = self.game.players[0].y + 2 * sin(self.game.players[0].theta)

        vecx = x1 - self.game.ghosts[0].x
        vecy = y1 - self.game.ghosts[0].y

        return [self.game.ghosts[0].x + 2 * vecx, self.game.ghosts[0].y + 2 * vecy]


class Clyde(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(2)
        #TODO This is hardcoded, fix
        self.wanderpoint = [57/2, 1/2]
        self.dot_threshold = 90

    def target(self):
        if pow(self.x - self.game.players[0].x, 2) + pow(self.y - self.game.players[0].y, 2) <= 64:
                return [30, -1]
        else:
            return self.wanderpoint