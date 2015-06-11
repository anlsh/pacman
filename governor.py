__author__ = 'anish'
from player import *
from ghosts import *

from time import time


class Governor:

    def __init__(self, game, handle="classic.map"):

        self.game = game
        self.master_state = "idle"

        game.players = []
        game.ghosts = []

        self.pup_time = None
        self.flash_time = None
        self.map_max_player = 0
        
        self.pup_duration = 10
        self.flash_duration = 2

        self.indefinite_chase = False

        self.start_time = time()
        self.now = self.start_time
        self.past = self.now - .1

        with open(handle) as f:

            lines = f.readlines()
            for l in lines:
                if "#" in l:
                    args = l.split()

                    if args[0] == "#MAX_PLAYERS":
                        self.map_max_players = int(args[1])

                    elif args[0] == "#PLAYERSPAWN" and len(self.game.players) < self.map_max_players and \
                        len(self.game.players) < self.game.wanted_players:

                        self.game.players.append(Player(self.game, args[1], args[2], len(self.game.players) + 1))

                    elif args[0] == "#BLINKYSPAWN":
                        self.game.ghosts.append(Blinky(self.game, args[1], args[2]))

                    elif args[0] == "#PINKYSPAWN":
                        self.game.ghosts.append(Pinky(self.game, args[1], args[2]))

                    elif args[0] == "#INKYSPAWN":
                        self.game.ghosts.append(Inky(self.game, args[1], args[2]))

                    elif args[0] == "#CLYDESPAWN":
                        self.game.ghosts.append(Clyde(self.game, args[1], args[2]))

    def update(self):

        if self.pup_time is not None and self.into_interval(self.pup_time + self.pup_duration,
                                                            self.pup_time + self.pup_duration + 1):

            self.set_ghost_states("flashing", break_scared=True, break_wander=False, break_chase=False)
            self.flash_time = time() - self.start_time
            self.pup_time = None

        if self.flash_time is not None and self.into_interval(self.flash_time + self.flash_duration,
                                                              self.flash_time + self.flash_duration + 1):

            self.set_ghost_states(self.master_state, break_scared=True, break_wander=False, break_chase=False)
            self.flash_time = None

        if self.game.level == 1:
            self.pup_duration = 9
            self.flash_duration = 3

            if self.into_interval(0, 7):
                self.master_state = "wander"
            elif self.into_interval(7, 27):
                self.master_state = "chase"
            elif self.into_interval(27, 34):
                self.master_state = "wander"
            elif self.into_interval(34, 54):
                self.master_state = "chase"
            elif self.into_interval(54, 59):
                self.master_state = "wander"
            elif self.into_interval(59, 79):
                self.master_state = "chase"
            elif self.into_interval(79, 84):
                self.master_state = "wander"
            elif self.into_interval(84, 87):
                self.master_state = "chase"
                print("permanent chase!")
                self.indefinite_chase = True

        elif 2 <= self.game.level <= 4:
            self.pup_duration = 5
            self.flash_duration = 3

            if self.into_interval(0, 7):
                self.master_state = "wander"
            elif self.into_interval(7, 27):
                self.master_state = "chase"
            elif self.into_interval(27, 34):
                self.master_state = "wander"
            elif self.into_interval(34, 54):
                self.master_state = "chase"
            elif self.into_interval(54, 59):
                self.master_state = "wander"
            elif self.into_interval(59, 1092):
                self.master_state = "chase"
            elif self.into_interval(1092, 1093):
                self.master_state = "wander"
            elif self.into_interval(1093, 2000):
                self.master_state = "chase"
                self.indefinite_chase = True

        else:

            self.pup_duration = 0
            self.flash_duration = 2

            if self.into_interval(0, 7):
                self.master_state = "wander"
            elif self.into_interval(7, 27):
                self.master_state = "chase"
            elif self.into_interval(27, 34):
                self.master_state = "wander"
            elif self.into_interval(34, 54):
                self.master_state = "chase"
            elif self.into_interval(54, 59):
                self.master_state = "wander"
            elif self.into_interval(59, 1096):
                self.master_state = "chase"
            elif self.into_interval(1096, 1097):
                self.master_state = "wander"
            elif self.into_interval(1097, 2000):
                self.master_state = "chase"
                self.indefinite_chase = True

        self.set_ghost_states(self.master_state)
        self.past = self.now
        self.now = time()

    def set_ghost_states(self, state, break_idle=False, break_scared=False, break_wander=True, break_chase=True):

        for g in self.game.ghosts:

            if g.state == "escape" or g.state == "retreat":
                continue

            elif (g.state == "scared" or g.state == "flashing") and break_scared:
                g.state = state

            elif state == "scared" and g.state != "scared" and g.state != "flashing" and g.state != "idle":
                g.theta = g.theta + 180 if g.theta < 180 else g.theta - 180
                g.state = state

            elif g.state == "wander" and break_wander:
                g.state = state

            elif g.state == "chase" and break_chase:
                g.state = state

            elif g.state == "idle" and break_idle:
                if state == "scared":
                    continue
                g.state = "escape" if not g.escaped else state

    def into_interval(self, start, stop):

        return start <= self.now - self.start_time < stop and not (start <= self.past - self.start_time < stop)

    def fire_pup(self):

        self.pup_time = time() - self.start_time
        self.set_ghost_states("scared")
