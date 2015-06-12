__author__ = 'anish'

from ghost import *


class Blinky(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(5)
        #TODO This is hardcoded, fix
        self.wanderpoint = [100, 100]
        self.dot_threshold = 0

    def target(self):
        return [self.target_player.x, self.target_player.y]


class Pinky(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(4)
        #TODO This is hardcoded, fix
        self.wanderpoint = [7/2, 61/2]
        self.dot_threshold = 30

    def target(self):

        try:
            return [self.target_player.x + 4 * cos(self.target_player.theta),
                                  self.target_player.y + 4 * sin(self.target_player.theta)]
        except TypeError:
            return self.wanderpoint

class Inky(Ghost):

    def __init__(self, game, x, y):

        super().__init__(game, x, y)
        self.load_resources(3)
        #TODO This is hardcoded, fix
        self.wanderpoint = [7/2, 1/2]
        self.dot_threshold = 60

    def target(self):
        try:
            x1 = self.target_player.x + 2 * cos(self.target_player.theta)
            y1 = self.target_player.y + 2 * sin(self.target_player.theta)
        except TypeError:
            return self.wanderpoint

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
        if pow(self.x - self.target_player.x, 2) + pow(self.y - self.target_player.y, 2) <= 64:
                return [30, -1]
        else:
            return self.wanderpoint