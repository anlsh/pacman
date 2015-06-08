__author__ = 'anish'
from time import time
from player import *
from ghost import *


class Governor:

    def __init__(self, game):

        self.game = game
        self.start_time = time()
        self.now = time()
        self.pre = 0
        self.pup_time = None
        self.flash_time = None

        self.pup_duration = 10
        self.flash_duration = 2

        self.indefinite_chase = False
        self.master_state = "idle"

        game.players = [Player([key.W, key.A, key.S, key.D], 15.5, 8.5, game)]
        game.ghosts = [Blinky(16.5, 16.5, game), Pinky(15.5, 16.5, game),
                        Inky(13.5, 16.5, game),  Clyde(18.5, 16.5, game)]

    def update(self):

        if self.pup_time is not None and self.pup_time + self.pup_duration <= time() < \
                                self.pup_time + self.pup_duration + 1:
            self.set_ghost_states("flashing", override_scared=True, override_wander=False, override_chase=False)
            self.flash_time = time()
            self.pup_time = None

        if self.flash_time is not None and self.flash_time + self.flash_duration <= time() < \
                                                          self.flash_time + self.flash_duration + 1:
            self.set_ghost_states(self.master_state, override_scared=True, override_wander=False, override_chase=False)
            self.flash_time = None

        if self.indefinite_chase:
            self.set_ghost_states("chase", override_idle=True)
            return None

        if self.game.level == 1:

            self.pup_duration = 10
            self.flash_duration = 2

            if self.into_time(0, 7):
                self.master_state = "wander"
            elif self.into_time(7, 27):
                self.master_state = "chase"
            elif self.into_time(27, 34):
                self.master_state = "wander"
            elif self.into_time(34, 54):
                self.master_state = "chase"
            elif self.into_time(54, 59):
                self.master_state = "wander"
            elif self.into_time(59, 79):
                self.master_state = "chase"
            elif self.into_time(79, 84):
                self.master_state = "wander"
            elif self.into_time(84, 87):
                self.master_state = "chase"
                self.indefinite_chase = True

        elif 2 <= self.game.level <= 4:
            self.pup_duration = 6
            self.flash_duration = 2

            if self.into_time(0, 7):
                self.master_state = "wander"
            elif self.into_time(7, 27):
                self.master_state = "chase"
            elif self.into_time(27, 34):
                self.master_state = "wander"
            elif self.into_time(34, 54):
                self.master_state = "chase"
            elif self.into_time(54, 59):
                self.master_state = "wander"
            elif self.into_time(59, 1092):
                self.master_state = "chase"
            elif self.into_time(1092, 1093):
                self.master_state = "wander"
            elif self.into_time(1093, 2000):
                self.master_state = "chase"
                self.indefinite_chase = True

        else:

            self.pup_duration = 0
            self.flash_duration = 2

            if self.into_time(0, 7):
                self.master_state = "wander"
            elif self.into_time(7, 27):
                self.master_state = "chase"
            elif self.into_time(27, 34):
                self.master_state = "wander"
            elif self.into_time(34, 54):
                self.master_state = "chase"
            elif self.into_time(54, 59):
                self.master_state = "wander"
            elif self.into_time(59, 1096):
                self.master_state = "chase"
            elif self.into_time(1096, 1097):
                self.master_state = "wander"
            elif self.into_time(1097, 2000):
                self.master_state = "chase"
                self.indefinite_chase = True

        self.set_ghost_states(self.master_state)

        self.pre = self.now
        self.now = time()

    def fire_pup(self):

        self.pup_time = time()
        self.set_ghost_states("scared")

    def set_ghost_states(self, state, override_idle=False, override_scared=False, override_wander=True,
                         override_chase=True):

        for g in self.game.ghosts:

            if g.state == "escape" or g.state == "retreat":
                continue

            elif (g.state == "scared" or g.state == "flashing") and override_scared:
                g.state = state

            elif state == "scared" and g.state != "scared" and g.state != "flashing" and g.state != "idle":
                g.theta = g.theta + 180 if g.theta < 180 else g.theta - 180
                g.state = state

            elif g.state == "wander" and override_wander:
                g.state = state

            elif g.state == "chase" and override_chase:
                g.state = state

            elif g.state == "idle" and override_idle:
                if state == "scared":
                    continue
                g.state = state

    def into_time(self, start, stop):

        return self.now - self.start_time >= start and self.now - self.start_time < stop and not \
            (self.pre - self.start_time >= start and self.pre -self.start_time < stop)