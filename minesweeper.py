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

def create_grid(width, height):
    """Creates a grid with the given width and height."""
    return [[0 for i in range(width)] for j in range(height)]


#Objects - object Cell
class Cell:
    def __init__(self, x, y, value, width = OBJ_WIDTH, height = OBJ_HEIGHT, hidden = True):
        self.x = x
        self.y = y
        self.pos_x = x // (OBJ_WIDTH + 2)
        self.pos_y = y // (OBJ_HEIGHT + 2)
        self.width = width
        self.height = height
        self.value = value
        self.hidden = hidden
        self.marked = False
    
    def blit(self):
        if self.hidden:
            if self.marked:
                pygame.draw.rect(screen, (0, 0, 250), (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        elif self.value == MINE:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
            screen.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (180, 180, 180), (self.x, self.y, self.width, self.height))
            if self.value != 0:
                screen.blit(self.img, (self.x, self.y))
    
    def reveal(self):
        self.hidden = False

    def is_mine(self):
        return self.value == MINE

    def is_empty(self):
        return self.value == 0


#Initialization.
pygame.init()

#Loading images to pygame.
mine_image = pygame.image.load(FILES + r"\mine.png")
image_0 = pygame.image.load(FILES + r"\0.png")
image_1 = pygame.image.load(FILES + r"\1.png")
image_2 = pygame.image.load(FILES + r"\2.png")
image_3 = pygame.image.load(FILES + r"\3.png")
image_4 = pygame.image.load(FILES + r"\4.png")
image_5 = pygame.image.load(FILES + r"\5.png")
image_6 = pygame.image.load(FILES + r"\6.png")
image_7 = pygame.image.load(FILES + r"\7.png")
image_8 = pygame.image.load(FILES + r"\8.png")
icon = pygame.image.load(FILES + r"\mine.png")

#Resizing the images.
mine_image = pygame.transform.scale(mine_image, (OBJ_WIDTH, OBJ_HEIGHT))
image_0 = pygame.transform.scale(image_0, (OBJ_WIDTH, OBJ_HEIGHT))
image_1 = pygame.transform.scale(image_1, (OBJ_WIDTH, OBJ_HEIGHT))
image_2 = pygame.transform.scale(image_2, (OBJ_WIDTH, OBJ_HEIGHT))
image_3 = pygame.transform.scale(image_3, (OBJ_WIDTH, OBJ_HEIGHT))
image_4 = pygame.transform.scale(image_4, (OBJ_WIDTH, OBJ_HEIGHT))
image_5 = pygame.transform.scale(image_5, (OBJ_WIDTH, OBJ_HEIGHT))
image_6 = pygame.transform.scale(image_6, (OBJ_WIDTH, OBJ_HEIGHT))
image_7 = pygame.transform.scale(image_7, (OBJ_WIDTH, OBJ_HEIGHT))
image_8 = pygame.transform.scale(image_8, (OBJ_WIDTH, OBJ_HEIGHT))

#Creating a dictionary of values and corresponding images.
DICT = {0: image_0, 1: image_1, 2: image_2, 3: image_3, 4: image_4, 5: image_5, 6: image_6, 7: image_7, 8: image_8, "X": mine_image}

#Screen, caption, icon, game variables and GUI settings.
screen = pygame.display.set_mode(SIZE)
pygame.display.set_icon(icon)
pygame.display.set_caption(CAPTION)
CLOCK = pygame.time.Clock()
TIMER = [0, 0]
has_activated_timer = False
GAME_OVER = False
GAME_WIN = False
REVEALED = False

#Music and sounds.
mixer.music.load(FILES + r"\background.wav")
mixer.music.play(-1)
kill_sound = mixer.Sound(FILES + r"\kill.wav")
winner_sound = mixer.Sound(FILES + r"\game_winner.wav")
has_played_winner_sound = False

#Font and text.
font = pygame.font.SysFont("Arial", 28)
white = (255, 255, 255)
space_text = font.render("SPACE:", True, white)
restart_text = font.render("Restart", True, white)
enter_text = font.render("ENTER:", True, white)
reveal_text = font.render("Show Mines", True, white)
rmb_text = font.render("RMB:", True, white)
flag_text = font.render("Flag", True, white)

#Instructions
def instructions():
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 200, 0, WIDTH, HEIGHT))
    stopwatch = font.render(f"TIME: {TIMER[1]}", True, white)
    screen.blit(stopwatch, (WIDTH - 175, 60))
    screen.blit(space_text, (WIDTH - 175, 170))
    screen.blit(restart_text, (WIDTH - 175, 202))
    screen.blit(rmb_text, (WIDTH - 175, 295))
    screen.blit(flag_text, (WIDTH - 175, 327))
    screen.blit(enter_text, (WIDTH - 175, 480))
    screen.blit(reveal_text, (WIDTH - 175, 512))

#Initialization of the grid and the cells.
def start_grid():
    return prepare_grid(distribute_mines(create_grid(MS_WIDTH, MS_HEIGHT)))

def start_cells(grid):
    return [[Cell((OBJ_WIDTH + 2)*x, (OBJ_HEIGHT + 2)*y, grid[y][x]) for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]

