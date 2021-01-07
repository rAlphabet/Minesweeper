class Settings:
    """Class to represent settings for Minesweeper."""
    def __init__(self):
        self.size = 9
    
    def change_size(self, new_size):
        """Changes the size (of the grid)."""
        self.size = new_size
    
    