import random
import pygame
from pygame import mixer

#Settings
class Settings:
    """Class to represent settings for Minesweeper."""
    def __init__(self):
        self.size = 9
        self.x_left = 164
        self.y = 128
        self.img = None
        self.is_open = False
        self.dictionary = None
        self.sound_img = {"on": None, "off": None}
    
    def change_size(self, new_size):
        """Changes the size (of the grid)."""
        self.size = new_size
    
    def set_img(self, img):
        """Sets the self.img to a specific image."""
        self.img = img
    
    def set_sound_img(self, img_on, img_off):
        """Sets the sound images to img_on and img_off."""
        self.sound_img["on"] = img_on
        self.sound_img["off"] = img_off
    
    def load_dict(self, dictionary):
        """Loads a dictionary to self.dictionary"""
        self.dictionary = dictionary

    def blit(self, width_of_grid):
        """Draws an image onto the screen."""
        if self.img != None:
            screen.blit(self.img, (width_of_grid - self.x_left ,self.y))
    
    def open_close(self):
        """Open or closes settings."""
        self.is_open = not self.is_open
    
    def show(self, width_of_grid, height_of_grid):
        """Displays settings menu onto the screen."""
        if self.is_open:
            pygame.draw.rect(screen, (125, 75, 255), (0, 0, width_of_grid, height_of_grid))
            Settings.blit(width_of_grid)
            screen.blit(self.dictionary[self.size][0], self.dictionary["pos"])
            for d, text in zip(self.dictionary.items(), [text_9x9, text_11x11, text_13x13, text_16x16, text_20x20, text_25x25, None]):
                if d[0] == self.size:
                    pygame.draw.rect(screen, (0, 0, 0), (d[1][1][0] - 8, d[1][1][1] - 3, 96, 39))
                    pygame.draw.rect(screen, (0, 255, 0), (d[1][1][0] - 5, d[1][1][1], 90, 33))
                if d[0] != "pos":
                    screen.blit(text, (d[1][1][0], d[1][1][1]))


#Constants, variables and path for the game.
Settings = Settings()
MINE = "X"
FILES = r"C:\Users\Mojca\Desktop\gitProjects\Minesweeper\files"
MS_WIDTH = MS_HEIGHT = Settings.size
OBJ_WIDTH = OBJ_HEIGHT = round(64 * (1 / (MS_WIDTH / 9)))
SIZE = WIDTH, HEIGHT = MS_WIDTH * (OBJ_WIDTH + 2) + 200, MS_HEIGHT * (OBJ_HEIGHT + 2) - 2
CAPTION = "Minesweeper"
FPS = 24

#Function to reset some of the variables above.
def reset_variables():
    """Resets certain variables to new values."""
    global MS_WIDTH, MS_HEIGHT, OBJ_WIDTH, OBJ_HEIGHT, WIDTH, HEIGHT, SIZE
    MS_WIDTH = MS_HEIGHT = Settings.size
    OBJ_WIDTH = OBJ_HEIGHT = round(64 * (1 / (MS_WIDTH / 9)))
    SIZE = WIDTH, HEIGHT = MS_WIDTH * (OBJ_WIDTH + 2) + 200, MS_HEIGHT * (OBJ_HEIGHT + 2) - 2


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


#Cell object
class Cell:
    """Class to represent a cell."""
    def __init__(self, x, y, value, width, height, hidden = True):
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
        global has_activated_timer, GAME_STOP
        has_activated_timer = False
        GAME_STOP = True
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
    global has_activated_timer, GAME_STOP
    if REVEALED:
        has_activated_timer = False
        GAME_STOP = True
        for cell in list_of_cells:
            if cell.value == MINE:
                mixer.music.stop()
                pygame.draw.rect(screen, (180, 180, 180), (cell.x, cell.y, cell.width, cell.height))
                screen.blit(mine_image, (cell.x, cell.y))

def is_finished():
    """Checks if player has won. If he has, it shows all the mines."""
    global GAME_STOP, has_played_winner_sound, has_activated_timer
    ANY_HIDDEN = False
    for cell in list_of_cells:
        if cell.value != MINE:
            if cell.hidden:
                ANY_HIDDEN = ANY_HIDDEN or cell.hidden
                break
    if not ANY_HIDDEN:
        GAME_STOP = True
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
settings_icon = pygame.image.load(FILES + r"\settings_icon.png")
setting9 = pygame.image.load(FILES + r"\setting9.png")
setting11 = pygame.image.load(FILES + r"\setting11.png")
setting13 = pygame.image.load(FILES + r"\setting13.png")
setting16 = pygame.image.load(FILES + r"\setting16.png")
setting20 = pygame.image.load(FILES + r"\setting20.png")
setting25 = pygame.image.load(FILES + r"\setting25.png")
sound_on = pygame.image.load(FILES + r"\sound_on.png")
sound_off = pygame.image.load(FILES + r"\sound_off.png")

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
settings_icon = pygame.transform.scale(settings_icon, (46, 46))
setting9 = pygame.transform.scale(setting9, (400, 400))
setting11 = pygame.transform.scale(setting11, (400, 400))
setting13 = pygame.transform.scale(setting13, (400, 400))
setting16 = pygame.transform.scale(setting16, (400, 400))
setting20 = pygame.transform.scale(setting20, (400, 400))
setting25 = pygame.transform.scale(setting25, (400, 400))
sound_on = pygame.transform.scale(sound_on, (46, 46))
sound_off = pygame.transform.scale(sound_off, (46, 46))

#Function to resize images when needed.
def resize_images():
    global mine_image, image_0, image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8
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
SETTINGS_DICT = {9: (setting9, (WIDTH - 175, 200)), 11: (setting11, (WIDTH - 175, 260)), 13: (setting13, (WIDTH - 175, 320)), 16: (setting16, (WIDTH - 175, 380)), 20: (setting20, (WIDTH - 175, 440)), 25: (setting25, (WIDTH - 175, 500)), "pos": (120, 100)}

#Function to remake DICT when needed.
def remake_dict():
    global DICT
    DICT = {0: image_0, 1: image_1, 2: image_2, 3: image_3, 4: image_4, 5: image_5, 6: image_6, 7: image_7, 8: image_8, "X": mine_image}

#Loading settings_icon into Settings object
Settings.set_img(settings_icon)
Settings.load_dict(SETTINGS_DICT)

#Screen, caption, icon, game variables and GUI settings.
screen = pygame.display.set_mode(SIZE)
pygame.display.set_icon(icon)
pygame.display.set_caption(CAPTION)
CLOCK = pygame.time.Clock()
TIMER = [0, 0]
has_activated_timer = False
GAME_OVER = False
GAME_STOP = False
REVEALED = False

#Music and sounds.
mixer.music.load(FILES + r"\background.wav")
kill_sound = mixer.Sound(FILES + r"\kill.wav")
winner_sound = mixer.Sound(FILES + r"\game_winner.wav")
has_played_winner_sound = False

#Font and text.
font = pygame.font.SysFont("Arial", 28, bold=True)
black = (0, 0, 0)
space_text = font.render("SPACE:", True, black)
restart_text = font.render("Restart", True, black)
enter_text = font.render("ENTER:", True, black)
reveal_text = font.render("Show Mines", True, black)
rmb_text = font.render("RMB:", True, black)
flag_text = font.render("Flag", True, black)

#Text for settings.
text_9x9 = font.render("9 x 9", True, black)
text_11x11 = font.render("11 x 11", True, black)
text_13x13 = font.render("13 x 13", True, black)
text_16x16 = font.render("16 x 16", True, black)
text_20x20 = font.render("20 x 20", True, black)
text_25x25 = font.render("25 x 25", True, black)

#Instructions
def instructions():
    """Draws text onto the screen (instructions and timer)."""
    pygame.draw.rect(screen, (125, 75, 255), (WIDTH - 200, 0, WIDTH, HEIGHT))
    stopwatch = font.render(f"TIME: {TIMER[1]}", True, black)
    screen.blit(stopwatch, (WIDTH - 175, 50))
    screen.blit(space_text, (WIDTH - 175, 226))
    screen.blit(restart_text, (WIDTH - 175, 258))
    screen.blit(rmb_text, (WIDTH - 175, 353))
    screen.blit(flag_text, (WIDTH - 175, 385))
    screen.blit(enter_text, (WIDTH - 175, 480))
    screen.blit(reveal_text, (WIDTH - 175, 512))

#Initialization of the grid and the cells.
def start_grid():
    """Creates the grid."""
    return prepare_grid(distribute_mines(create_grid(MS_WIDTH, MS_HEIGHT)))

def start_cells(grid):
    """Creates Cell objects corresponding to the grid."""
    return [[Cell((OBJ_WIDTH + 2)*x, (OBJ_HEIGHT + 2)*y, grid[y][x], OBJ_WIDTH, OBJ_HEIGHT) for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]

def start_list_cells(cells):
    """Creates a list of cells that stores all the Cell objects.
    List of cells is a 1-D list."""
    return [cells[j][i] for i in range(dim(grid)["x"]) for j in range(dim(grid)["y"])]

#Game start and restart.
def restart_game():
    """Restarts the game with setting certain variables to their initial values
    and creating a new grid along with new Cell objects."""
    global screen, TIMER, has_activated_timer, GAME_OVER, GAME_STOP, REVEALED, has_played_winner_sound, grid, cells, list_of_cells
    mixer.music.play(-1)
    screen = pygame.display.set_mode(SIZE)
    TIMER = [0, 0]
    has_activated_timer = False
    GAME_OVER = False
    GAME_STOP = False
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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

            s = screen.blit(Settings.img, (WIDTH - Settings.x_left, Settings.y))
            if s.collidepoint(position):
                if event.button == 1:
                    Settings.is_open = not Settings.is_open
            
            if Settings.is_open:
                for d, text in zip(Settings.dictionary.items(), [text_9x9, text_11x11, text_13x13, text_16x16, text_20x20, text_25x25, None]):
                    if d[0] != "pos":
                        g = screen.blit(text, (d[1][1][0], d[1][1][1]))
                        if g.collidepoint(position):
                            if event.button == 1:
                                Settings.change_size(d[0])
                                reset_variables()
                                resize_images()
                                remake_dict()
                                restart_game()

            if not GAME_STOP and not Settings.is_open:
                for cell in list_of_cells:
                    b = screen.blit(cell.img, (cell.x, cell.y))
                    if b.collidepoint(position):
                        if event.button == 1:
                            if not has_activated_timer:
                                has_activated_timer = True
                            cell.check_cell()
                        elif event.button == 3:
                            cell.marked = not cell.marked

    if Settings.is_open:
        Settings.show(WIDTH, HEIGHT)
    else:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

        for cell in list_of_cells:
            cell.blit()

        if has_activated_timer:
            timer()
        
        instructions()
        Settings.blit(WIDTH)
        reveal_all()
        is_finished()
    pygame.display.update()

