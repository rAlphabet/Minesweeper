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

def is_in_grid(x, y, grid):
    """Checks if (x, y) position is inside the grid."""
    if 0 <= x < dim(grid)["x"] and 0 <= y < dim(grid)["y"]:
        return True
    else: return False

def surrounding_mines(x, y, grid):
    f"""Counts and returns mines around (x, y) position if (x, y) is not a mine.
    If (x, y) is a mine, it returns MINE ({MINE})."""
    if is_mine(x, y, grid):
        return MINE
    return sum(1 for i in range(-1, 2) for j in range(-1, 2) if (x, y) != (x+i, y+j) and is_in_grid(x+i, y+j, grid) and is_mine(x+i, y+j, grid))

def prepare_grid(grid, copy = True):
    """Prepares the grid, so it has all the attributes:
    mines, empty spaces, numbers. If copy is set to True,
    the function returns new prepared grid."""
    if copy:
        return [[surrounding_mines(x, y, grid) for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]
    else:
        for y in range(dim(grid)["y"]):
            for x in range(dim(grid)["x"]):
                grid[y][x] = surrounding_mines(x, y, grid)

def probability_array(density):
    """Creates a probability array of values True and False"""
    density *= 100
    return [True if i < density else False for i in range(100)]

def distribute_mines(grid, density = 0.12, copy = True):
    """Distributes mines to the grid. If copy is set to True,
    the function returns new grid with distributed mines.
    Density decides how much % of the grid should be mines."""
    prob = probability_array(density)
    if copy:
        return [[MINE if random.choice(prob) else 0 for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]
    else:
        for y in range(dim(grid)["y"]):
            for x in range(dim(grid)["x"]):
                if random.choice(prob):
                    grid[y][x] = MINE

