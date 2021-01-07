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
    """Class to represent a cell."""
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
        self.img = DICT[value]
   
    def blit(self):
        """This method draws Cell content onto the screen."""
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
        """Reveals the hidden Cell."""
        self.hidden = False

    def is_mine(self):
        """Checks if this cell is a mine."""
        return self.value == MINE

    def is_empty(self):
        """Checks if this cell is an empty one."""
        return self.value == 0

    def check_cell(self):
        """Checks the current Cell. If it is empty, it recursively checks all the neighbour cells.
        If it is a mine, it calls the game_over method and the game ends. It also reveals the Cell."""
        if self.value == 0:
            self.reveal()
            neighbours = [(self.pos_x+i, self.pos_y+j) for i in range(-1, 2) for j in range(-1, 2) if (self.pos_x, self.pos_y) != (self.pos_x+i, self.pos_y+j) and is_in_grid(self.pos_x+i, self.pos_y+j, grid)]
            for coordinates in neighbours:
                neighbour_cell = cells[coordinates[1]][coordinates[0]]
                if neighbour_cell.hidden:
                    neighbour_cell.check_cell()
        else:
            self.reveal()
            if self.value == MINE:
                self.game_over()

    def game_over(self):
        """Ends the game with setting certain variables to their initial values."""
        global has_activated_timer
        has_activated_timer = False
        mixer.music.stop()
        kill_sound.play()
        for cell in list_of_cells:
            if cell.value == MINE:
                cell.reveal()


#Functions for game functionality.
def timer():
    """Working stopwatch that counts seconds accordingly to the previously set FPS."""
    global TIMER
    TIMER[0] += 1
    if TIMER[0] == FPS:
        TIMER[0] = 0
        TIMER[1] += 1

def reveal_all():
    """Reveals all the mines."""
    global GAME_WIN
    if REVEALED:
        GAME_WIN = True
        for cell in list_of_cells:
            if cell.value == MINE:
                mixer.music.stop()
                pygame.draw.rect(screen, (180, 180, 180), (cell.x, cell.y, cell.width, cell.height))
                screen.blit(mine_image, (cell.x, cell.y))

def is_finished():
    """Checks if player has won. If he has, it shows all the mines."""
    global GAME_WIN
    ANY_HIDDEN = False
    global has_played_winner_sound
    global has_activated_timer
    for cell in list_of_cells:
        if cell.value != MINE:
            if cell.hidden:
                ANY_HIDDEN = ANY_HIDDEN or cell.hidden
                break
    if not ANY_HIDDEN:
        GAME_WIN = True
        has_activated_timer = False
        mixer.music.stop()
        for cell in list_of_cells:
            if cell.value == MINE:
                if not has_played_winner_sound:
                    winner_sound.play()
                    has_played_winner_sound = True
                pygame.draw.rect(screen, (0, 255, 0), (cell.x, cell.y, cell.width, cell.height))
                screen.blit(mine_image, (cell.x, cell.y))


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
    """Draws text onto the screen (instructions and timer)."""
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
    """Creates the grid."""
    return prepare_grid(distribute_mines(create_grid(MS_WIDTH, MS_HEIGHT)))

def start_cells(grid):
    """Creates Cell objects corresponding to the grid."""
    return [[Cell((OBJ_WIDTH + 2)*x, (OBJ_HEIGHT + 2)*y, grid[y][x]) for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]

def start_list_cells(cells):
    """Creates a list of cells that stores all the Cell objects.
    List of cells is a 1-D list."""
    return [cells[j][i] for i in range(dim(grid)["x"]) for j in range(dim(grid)["y"])]

#Game start and restart.
def restart_game():
    """Restarts the game with setting certain variables to their initial values
    and creating a new grid along with new Cell objects."""
    mixer.music.play(-1)
    global TIMER
    global has_activated_timer
    global GAME_OVER
    global GAME_WIN
    global REVEALED
    global has_played_winner_sound
    global grid
    global cells
    global list_of_cells
    TIMER = [0, 0]
    has_activated_timer = False
    GAME_OVER = False
    GAME_WIN = False
    REVEALED = False
    has_played_winner_sound = False
    grid = start_grid()
    cells = start_cells(grid)
    list_of_cells = start_list_cells(cells)


#Game loop.
restart_game()

running = True
while running:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restart_game()
            elif event.key == pygame.K_RETURN:
                REVEALED = True
        
        if not GAME_WIN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for cell in list_of_cells:
                    b = screen.blit(cell.img, (cell.x, cell.y))
                    if b.collidepoint(position):
                        if event.button == 1:
                            if not has_activated_timer:
                                has_activated_timer = True
                            cell.check_cell()
                        elif event.button == 3:
                            cell.marked = not cell.marked

    for cell in list_of_cells:
        cell.blit()

    if has_activated_timer:
        timer()
    
    instructions()
    reveal_all()
    is_finished()
    pygame.display.update()

