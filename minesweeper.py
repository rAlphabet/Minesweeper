import random
import pygame
from pygame import mixer

#Constants, variables and path for the game.
MINE = "X"
FILES = r"C:\Users\Mojca\Desktop\gitProjects\Minesweeper\files"
MS_WIDTH = 9
MS_HEIGHT = 9
OBJ_WIDTH = round(64 * (1 / (MS_WIDTH/9)))
OBJ_HEIGHT = round(64 * (1 / (MS_HEIGHT/9)))
SIZE = WIDTH, HEIGHT = MS_WIDTH * (OBJ_WIDTH + 2) + 200, MS_HEIGHT * (OBJ_HEIGHT + 2) - 2
CAPTION = "Minesweeper"
FPS = 24


#Algorithms for minesweeper's grid.
def is_mine(x, y, grid):
    """Checks if (x, y) position in the grid is a mine."""
    if grid[y][x] == MINE:
        return True
    else: return False

def dim(grid):
    """Returns a dictionary with keys 'x' and 'y' and
    values width and height of the given grid."""
    return {"x": len(grid[0]), "y": len(grid)}

