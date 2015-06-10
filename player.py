__author__ = 'anish'

from entity import *
from common import *
from pyglet.window import key
from sprite import Sprite
from copy import copy


class Player(Entity):

    def __init__(self, game, x, y, playernum):

        super().__init__(x, y, game)

        if playernum == 1:
            self.cscheme = [key.UP, key.LEFT, key.DOWN, key.RIGHT]
        elif playernum == 2:
            self.cscheme = [key.W, key.A, key.S, key.D]

        # movement related variables specific to how a player move
        self.want_theta = None
        self.last_theta = None
        self.horizontal_mismatch = False
        self.vertical_mismatch = False

        # control scheme, contains pyglet.key objects in directions up, left, down, right
        # handler to which a new state is pushed every iteration by the driver class
        self.keys = key.KeyStateHandler()

        # All variables needed for graphics only, although they might seem more important
        self.count = 0
        self.last_x = self.x
        self.last_y = self.y

        # Just declaring this here for consistency
        self.sprites = []

        # Load normal_sprites into an array which can be looped through
        self.load_resources()

    def load_resources(self):

        '''
        :WARNING: This entire method is heavily dependent on pyglet-specific methods. It will need to be reworked if
        a port is attempted
        '''
        # Slice out the needed region of the sprite sheet (32 x 32 Pac-Man normal_sprites) <pyglet>
        spritesheet = Entity.spritesheet.get_region(0, Entity.spritesheet.height - 32, 3 * 32, 32)

        # Convert the image into an array of images, and center their anchor points <pyglet>
        self.sprites = image.ImageGrid(spritesheet, 1, 3, item_width=32, item_height=32)
        for i in range(len(self.sprites)):
            self.sprites[i].anchor_x = self.sprites[i].width // 2
            self.sprites[i].anchor_y = self.sprites[i].width // 2

        # Convert the images in the array to normal_sprites <pyglet>
        self.sprites = [Sprite(i, self.game.graphics_group) for i in self.sprites]

        # Now store the normal_sprites in a dictionary indexed by frame and rotation angle
        temp_sprites = self.sprites
        self.sprites = {}
        for frame in range(len(temp_sprites)):
            angles = {}
            for x in [0, 90, 180, 270]:
                angles[x] = copy(temp_sprites[frame])
                angles[x].set_rotation(x)

            self.sprites[frame] = angles

        # Shift the frames cyclically to make the animation start with the pizza frame. If more frames are added
        # to the animation, this will need to be changed

        #After modifications are carried out, the animation is in the order pizza -> more eaten pizza -> circle
        c = self.sprites[0]
        self.sprites[0] = self.sprites[1]
        self.sprites[1] = self.sprites[2]
        self.sprites[2] = c

    def update_movement_possibilities(self):

        # Pac Man can actually start moving before he reaches the center of an open tile. To account for this, some
        # conditions besides whether the immediate tile is a block are taken into account
        self.can_right = True \
            if self.game.grid[int(self.y)][int(self.x) + 1] != "b" else self.x % 1 < 0.5

        self.can_left = True \
            if self.game.grid[int(self.y)][int(self.x) - 1] != "b" else self.x % 1 > 0.5

        self.can_up = True \
            if self.game.grid[int(self.y) + 1][int(self.x)] != "b" else self.y % 1 < 0.5

        self.can_down = True \
            if self.game.grid[int(self.y) - 1][int(self.x)] != "b" else self.y % 1 > 0.5

    def update(self):

        #update the wanted direction based upon which key is pressed
        if self.keys[self.cscheme[0]]:
            self.want_theta = 90
        elif self.keys[self.cscheme[1]]:
            self.want_theta = 180
        elif self.keys[self.cscheme[2]]:
            self.want_theta = 270
        elif self.keys[self.cscheme[3]]:
            self.want_theta = 0

        # Needed for mismatch correction, addressed farther down
        temp_theta = self.theta

        # Update the, well, you can understand this... This block is necessary for Player.draw to detect whether
        # the player has moved at all
        self.last_x = self.x
        self.last_y = self.y

        # Also self explanatory
        self.update_movement_possibilities()

        # If the player hasnt given any inputs yet, we just break out
        if self.want_theta is None:
            return None

        # This part of the code is a bit of a hellhole... even I dont fully understand it anymore, and I'm loathe to
        # touch any of it in the hopes of breaking it. However, I'll do my best to explain it.

        # If you want to go in a direction and there is not a block in said direction, check further conditions

        # FURTHER CONDITIONS
        # First condition: If you were just moving in a direction opposite to x, you can go direction x
        # Second condition: If there's a block in the direction you want to go, you cant turn
        # Third and Fourth conditions: If you've moved past the center of the block you want to turn into, you cant
        #       turn. Since whether you are past the center depends on which direction you approach it from (ie theta),
        #       an or statement with two cases is used

        if self.want_theta == 0 and self.can_right:
            if self.theta == 180 or (self.game.grid[int(self.y)][int((self.x + self.speed)) + 1] != "b") \
                and ((self.theta == 90 and self.y % 1 <= 0.5) or
                (self.theta == 270 and self.y % 1 >= 0.5) or self.theta is None):
                    self.theta = self.want_theta

        elif self.want_theta == 180 and self.can_left:
            if self.theta == 0 or (self.game.grid[int(self.y)][int((self.x - self.speed)) - 1] != "b") \
                and ((self.theta == 90 and self.y % 1 <= 0.5) or
                (self.theta == 270 and self.y % 1 >= 0.5) or self.theta is None):
                    self.theta = self.want_theta

        elif self.want_theta == 90 and self.can_up:
            if self.theta == 270 or (self.game.grid[int((self.y + self.speed)) + 1][int(self.x)] != "b") \
                and ((self.theta == 0 and self.x % 1 <= 0.5) or
                (self.theta == 180 and self.x % 1 >= 0.5) or self.theta is None):
                    self.theta = self.want_theta

        elif self.want_theta == 270 and self.can_down:
            if self.theta == 90 or (self.game.grid[int((self.y - self.speed)) - 1][int(self.x)] != "b") \
                and ((self.theta == 0 and self.x % 1 <= 0.5) or
                (self.theta == 180 and self.x % 1 >= 0.5) or self.theta is None):
                    self.theta = self.want_theta

        # Actually update the position. I'm not actually sure if all of these if statements are needed, but I'm too
        # scared and tired to find out

        if self.theta == 0 and self.can_right:
            self.x += self.speed * cos(self.theta).__int__()

        elif self.theta == 180 and self.can_left:
            self.x += self.speed * cos(self.theta).__int__()

        elif self.theta == 90 and self.can_up:
            self.y += self.speed * sin(self.theta).__int__()

        elif self.theta == 270 and self.can_down:
            self.y += self.speed * sin(self.theta).__int__()

        # Correct mismatches. Since Pac-Man is allowed to move before he actually reaches a turn per se, the last block
        # takes care of making sure that he always stays in the center of the path
        if temp_theta != self.theta:
            self.last_theta = temp_theta

        # Only do mismatch correction if the direction change is perpendicular

        self.horizontal_mismatch = (self.theta == 90 or self.theta == 270) \
                                        and (self.last_theta == 0 or self.last_theta == 180)

        self.vertical_mismatch = (self.theta == 0 or self.theta == 180) \
                                        and (self.last_theta == 90 or self.last_theta == 270)

        # Keep Pac Man moving in his last direction until the mismatch is fixed

        if self.horizontal_mismatch:
            if self.x % 1 != 0.5:
                self.x += self.speed * cos(self.last_theta).__int__()
            else:
                self.horizontal_mismatch = False

        elif self.vertical_mismatch:
            if self.y % 1 != 0.5:
                self.y += self.speed * sin(self.last_theta).__int__()
            else:
                self.vertical_mismatch = False

    def draw(self):

        # Update the count by some value. (.25 + .125) / 2 seems to work well
        if self.last_x != self.x or self.y != self.last_y:
            self.count += (.25 + .125) / 2

        #Based on the count and the current theta, draw a frame rotated at the appropriate angle
        try:
            self.sprites[int(self.count % 3)][self.theta].set_position(int(self.x * GRID_DIM), int(self.y * GRID_DIM))
            self.sprites[int(self.count % 3)][self.theta].draw()
        except KeyError:
            self.sprites[0][0].set_position(self.x * GRID_DIM, self.y * GRID_DIM)
            self.sprites[0][0].draw()