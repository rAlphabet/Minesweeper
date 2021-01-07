class Settings:
    """Class to represent settings for Minesweeper."""
    def __init__(self):
        self.size = 9
        self.x_left = 164
        self.y = 128
    
    def change_size(self, new_size):
        """Changes the size (of the grid)."""
        self.size = new_size
    
    