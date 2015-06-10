__author__ = 'anish'
from player import *
from ghosts import *


class Governor:

    def __init__(self, game, handle="classic.map"):

        self.game = game

        with open(handle) as f:

            lines = f.readlines()
            map_max_players = 2
            for l in lines:
                if "#" in l:
                    args = l.split()

                    if args[0] == "#MAX_PLAYERS":
                        map_max_players = int(args[1])

                    elif args[0] == "#PLAYERSPAWN" and len(self.game.players) < map_max_players and \
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
