class Map:
    '''
    Simple class to read a map from a text file and parse it
    '''
    def __init__(self, handle):
    #Pacman map is 28 by 31 just by url http://upload.wikimedia.org/wikipedia/en/5/59/Pac-man.png
        with open(handle) as f:
            self.grid = list(reversed(f.readlines()))
            self.grid = [list(self.grid[z])[0:-1] for z in range(len(self.grid))]
            for x in range(len(self.grid)):
                for y in range(len(self.grid[x])):
                    self.grid[x][y] = Tile(self.grid[x][y])
      
class Tile:
    '''
    class to represent a tile object
    '''
    def __init__(self, param):
        '''
        parameters -- b = block, d = dot, p = Pup
        warp tiles should be specified as *u* where u is not another
        established parameter, where each warp tile will warp to the 
        other tile with param *u*
        '''
        self.imglist = {"b":"block.png", "d":"dot.png", "p":"Pup.png", "e":"empty.png"}
        
        self.entity = None
        self.id = param
    
    def draw(self, context):
        raise NotImplementedError
