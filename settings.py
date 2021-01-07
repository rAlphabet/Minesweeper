class Settings:
    """Class to represent settings for Minesweeper."""
    def __init__(self):
        self.size = 9
        self.x_left = 164
        self.y = 128
        self.img = None
    
    def change_size(self, new_size):
        """Changes the size (of the grid)."""
        self.size = new_size
    
    def set_img(self, img):
        """Sets the self.img to a specific image."""
        self.img = img

    def blit(self, width_of_grid):
        """Draws an image 'img' onto the screen."""
        if self.img != None:
            screen.blit(self.img, (width_of_grid - self.x_left ,self.y))
    
    