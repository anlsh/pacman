__author__ = 'anish'
from entity import *


class Ghost(Entity):

    # TODO make the class use sprites

    def __init__(self, x, y, map, want_x=None, want_y=None):

        super().__init__(x, y, map)

        # setpoint coordinates
        self.want_x = None
        self.want_y = None

        if want_x is None or want_y is None:
            self.set_setpoint(x, y)
        else:
            self.set_setpoint(want_x, want_y)

    def update_movement_possibilities(self):
        '''
        Method meant to calculate possible directions the entity can go in. This does not account for the no-reversal
        rule- that is taken care of in the update method. This simply tests for a block in the desired position
        :return: None
        '''
        #The .000001 is included to make sure that the method correctly detects the presence of a block on the map
        # The constant's value does not matter, but it should be smaller than 1 / self.speed
        self.can_up = self.x % 1 == 0.5 and self.map.grid[int(self.y + 0.5)][int(self.x)] != "b"
        self.can_left = self.y % 1 == 0.5 and self.map.grid[int(self.y)][int(self.x - 0.5 - .00000001)] != "b"
        self.can_down = self.x % 1 == 0.5 and self.map.grid[int(self.y - 0.5 - .000000001)][int(self.x)] != "b"
        self.can_right = self.y % 1 == 0.5 and self.map.grid[int(self.y)][int(self.x + 0.5)] != "b"

    def set_setpoint(self, x, y):
        '''
        :param x: x position of setpoint
        :param y: y position of setpoint
        :return: None
        '''
        self.want_x = x
        self.want_y = y

    def update(self):
        '''
        Moves the ghost towards the player
        :return: None
        '''
        # TODO Implement targeting for multiple players if I have time

        self.update_movement_possibilities()

        # The AI attempts to take the shortest path to target. The squares of the distances are actually used to avoid
        # having to call math.sqrt
        up_distance = pow(self.x - self.want_x, 2) + pow(self.y + self.speed - self.want_y, 2)
        left_distance = pow(self.x - self.speed - self.want_x, 2) + pow(self.y - self.want_y, 2)
        down_distance = pow(self.x - self.want_x, 2) + pow(self.y - self.speed - self.want_y, 2)
        right_distance = pow(self.x + self.speed - self.want_x, 2) + pow(self.y - self.want_y, 2)

        distances = [right_distance, left_distance, down_distance, up_distance]

        if self.x != self.want_x or self.y != self.want_y:

            # This loop is needed to ensure that a valid theta is always set. If this is not included then sometimes an
            # appropriate theta will not be set because it is not the shortest path, allowing invalid paths to be taken

            theta_set = False

            while not theta_set:

                min_distance = min(distances)

                if self.can_up and up_distance == min_distance and self.theta != 270:
                    self.theta = 90
                    theta_set = True

                elif self.can_left and left_distance == min_distance and self.theta != 0:
                    self.theta = 180
                    theta_set = True

                elif self.can_down and down_distance == min_distance and self.theta != 90:
                    self.theta = 270
                    theta_set = True

                elif self.can_right and right_distance == min_distance and self.theta != 180:
                    self.theta = 0
                    theta_set = True

                #if none of the minimum distances are in valid directions, remove them from consideration and reloop
                for x in range(len(distances)):
                    try:
                        distances.remove(min_distance)
                    except ValueError:
                        break

            #update position
            self.x += self.speed * cos(self.theta).__int__()
            self.y += self.speed * sin(self.theta).__int__()

    def draw(self):
        '''
        Draw the appropriate sprite to the map
        :return: None
        '''
        # TODO Right now this just draws a box, I need to make it draw sprites
        self.map.draw_rectangle(self.x * GRID_DIM - GRID_DIM / 2, self.y * GRID_DIM - GRID_DIM / 2, GRID_DIM, GRID_DIM)