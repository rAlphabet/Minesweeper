import os
import random
import pygame
from pygame import mixer

#Settings
class Settings:
    """Class to represent settings for Minesweeper."""
    def __init__(self, size = 9):
        self.size = size
        self.x_left = 164
        self.y = 128
        self.img = None
        self.is_open = False
        self.dictionary = None
        self.sound_img = {"on": None, "off": None}
        self.is_sound = True
    
    def make(self):
        return self
    
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
            screen.blit(self.sound_img["on"], (width_of_grid - 100, 40))
            if not self.is_sound:
                screen.blit(self.sound_img["off"], (width_of_grid - 100, 40))

#Initialization of Settings.
Settings = Settings()


#Algorithms for minesweeper's grid.
def is_mine(x, y, grid):
    """Checks if (x, y) position in the grid is a mine."""
    if grid[y][x] == Game.MINE:
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
    If (x, y) is a mine, it returns Game.MINE ({Game.MINE})."""
    if is_mine(x, y, grid):
        return Game.MINE
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
        return [[Game.MINE if random.choice(prob) else 0 for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]
    else:
        for y in range(dim(grid)["y"]):
            for x in range(dim(grid)["x"]):
                if random.choice(prob):
                    grid[y][x] = Game.MINE

def create_grid(width, height):
    """Creates a grid with the given width and height."""
    return [[0 for i in range(width)] for j in range(height)]

#Functions to create the grid and the cells.
def start_grid(mw, mh):
    """Creates the grid."""
    return prepare_grid(distribute_mines(create_grid(mw, mh)))

def start_cells(grid, ow, oh):
    """Creates Cell objects corresponding to the grid."""
    return [[Cell((ow + 2)*x, (oh + 2)*y, grid[y][x], ow, oh) for x in range(dim(grid)["x"])] for y in range(dim(grid)["y"])]

def start_list_cells(cells):
    """Creates a list of cells that stores all the Cell objects.
    List of cells is a 1-D list."""
    return [cells[j][i] for i in range(dim(cells)["x"]) for j in range(dim(cells)["y"])]


#Cell object
class Cell:
    """Class to represent a cell."""
    def __init__(self, x, y, value, width, height, hidden = True):
        self.x = x
        self.y = y
        self.pos_x = x // (Game.OBJ_WIDTH + 2)
        self.pos_y = y // (Game.OBJ_HEIGHT + 2)
        self.width = width
        self.height = height
        self.value = value
        self.hidden = hidden
        self.marked = False
        self.img = Game.DICT[value]
   
    def blit(self):
        """This method draws Cell content onto the screen."""
        if self.hidden:
            if self.marked:
                pygame.draw.rect(screen, (0, 0, 250), (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        elif self.value == Game.MINE:
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
        return self.value == Game.MINE

    def is_empty(self):
        """Checks if this cell is an empty one."""
        return self.value == 0

    def check_cell(self):
        """Checks the current Cell. If it is empty, it recursively checks all the neighbour cells.
        If it is a mine, it calls the game_over method and the game ends. It also reveals the Cell."""
        if self.value == 0:
            self.reveal()
            neighbours = [(self.pos_x+i, self.pos_y+j) for i in range(-1, 2) for j in range(-1, 2) if (self.pos_x, self.pos_y) != (self.pos_x+i, self.pos_y+j) and is_in_grid(self.pos_x+i, self.pos_y+j, Game.grid)]
            for coordinates in neighbours:
                neighbour_cell = Game.cells[coordinates[1]][coordinates[0]]
                if neighbour_cell.hidden:
                    neighbour_cell.check_cell()
        else:
            self.reveal()
            if self.value == Game.MINE:
                self.game_over()

    def game_over(self):
        """Ends the game with setting certain variables to their initial values."""
        global has_activated_timer, GAME_STOP
        has_activated_timer = False
        GAME_STOP = True
        mixer.music.stop()
        kill_sound.play()
        for cell in Game.list_of_cells:
            if cell.value == Game.MINE:
                cell.reveal()


#Class Game (constants, variables and path for the game).
class Game:
    def __init__(self):
        self.MINE = "X"
        self.CAPTION = "Minesweeper"
        self.FPS = 24
        self.FILES = os.getcwd() + r"/files"
        self.MS_WIDTH = self.MS_HEIGHT = Settings.size
        self.OBJ_WIDTH = self.OBJ_HEIGHT = round(64 * (1 / (self.MS_WIDTH / 9)))
        self.SIZE = self.WIDTH, self.HEIGHT = self.MS_WIDTH * (self.OBJ_WIDTH + 2) + 200, self.MS_HEIGHT * (self.OBJ_HEIGHT + 2) - 2
        self.TIMER = [0, 0]
        self.DICT = None
        self.GAME_STOP = False
        self.has_activated_timer = True
        self.REVEALED = False
        self.has_played_winner_sound = False
        self.list_of_cells = None
    
    def make(self):
        return self

    def loc(self):
        self.list_of_cells = start_list_cells(start_cells(start_grid(self.MS_WIDTH, self.MS_HEIGHT), self.OBJ_WIDTH, self.OBJ_HEIGHT))

    def reset_size(self, mw, mh, ow, oh, w, h, size):
        self.MS_WIDTH = self.MS_HEIGHT = Settings.size
        self.OBJ_WIDTH = self.OBJ_HEIGHT = round(64 * (1 / (self.MS_WIDTH / 9)))
        self.SIZE = self.WIDTH, self.HEIGHT = self.MS_WIDTH * (self.OBJ_WIDTH + 2) + 200, self.MS_HEIGHT * (self.OBJ_HEIGHT + 2) - 2
    
    def remake_dict(self):
        self.DICT = {0: image_0, 1: image_1, 2: image_2, 3: image_3, 4: image_4, 5: image_5, 6: image_6, 7: image_7, 8: image_8, "X": mine_image}

    def timer(self):
        """Working stopwatch that counts seconds accordingly to the previously set Game.FPS."""
        self.TIMER[0] += 1
        if self.TIMER[0] == self.FPS:
            self.TIMER[0] = 0
            self.TIMER[1] += 1

    def reveal_all(self):
        """Reveals all the mines."""
        if self.REVEALED:
            self.has_activated_timer = False
            self.GAME_STOP = True
            for cell in self.list_of_cells:
                if cell.value == self.MINE:
                    mixer.music.stop()
                    pygame.draw.rect(screen, (180, 180, 180), (cell.x, cell.y, cell.width, cell.height))
                    screen.blit(mine_image, (cell.x, cell.y))

    def is_finished(self):
        """Checks if player has won. If he has, it shows all the mines."""
        ANY_HIDDEN = False
        for cell in self.list_of_cells:
            if cell.value != self.MINE:
                if cell.hidden:
                    ANY_HIDDEN = ANY_HIDDEN or cell.hidden
                    break
        if not ANY_HIDDEN:
            self.GAME_STOP = True
            self.has_activated_timer = False
            mixer.music.stop()
            for cell in self.list_of_cells:
                if cell.value == self.MINE:
                    if not self.has_played_winner_sound:
                        winner_sound.play()
                        self.has_played_winner_sound = True
                    pygame.draw.rect(screen, (0, 255, 0), (cell.x, cell.y, cell.width, cell.height))
                    screen.blit(mine_image, (cell.x, cell.y))
    
    def restart(self):
        self.grid = create_grid(self.MS_WIDTH, self.MS_HEIGHT)
        self.cells = start_cells(self.grid, self.OBJ_WIDTH, self.OBJ_HEIGHT)
        self.loc()
        

#Initialization of Game.
Game = Game()

#Initialization.
pygame.init()

#Loading images to pygame.
icon = pygame.image.load(Game.FILES + r"/mine.png")

#Function to resize images when needed.
def resize_image(path, w, h):
    """Loads and resizes images."""
    temp = pygame.image.load(path)
    return pygame.transform.scale(temp, (w, h))

mine_image = resize_image(Game.FILES + r"/mine.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_0 = resize_image(Game.FILES + r"/0.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_1 = resize_image(Game.FILES + r"/1.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_2 = resize_image(Game.FILES + r"/2.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_3 = resize_image(Game.FILES + r"/3.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_4 = resize_image(Game.FILES + r"/4.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_5 = resize_image(Game.FILES + r"/5.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_6 = resize_image(Game.FILES + r"/6.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_7 = resize_image(Game.FILES + r"/7.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
image_8 = resize_image(Game.FILES + r"/8.png", Game.OBJ_WIDTH, Game.OBJ_HEIGHT)
settings_icon = resize_image(Game.FILES + r"/settings_icon.png", 46, 46)
setting9 = resize_image(Game.FILES + r"/setting9.png", 400, 400)
setting11 = resize_image(Game.FILES + r"/setting11.png", 400, 400)
setting13 = resize_image(Game.FILES + r"/setting13.png", 400, 400)
setting16 = resize_image(Game.FILES + r"/setting16.png", 400, 400)
setting20 = resize_image(Game.FILES + r"/setting20.png", 400, 400)
setting25 = resize_image(Game.FILES + r"/setting25.png", 400, 400)
sound_on = resize_image(Game.FILES + r"/sound_on.png", 46, 46)
sound_off = resize_image(Game.FILES + r"/sound_off.png", 46, 46)

#Creating a dictionary of values and corresponding images.
SETTINGS_DICT = {9: (setting9, (Game.WIDTH - 175, 200)), 11: (setting11, (Game.WIDTH - 175, 260)), 13: (setting13, (Game.WIDTH - 175, 320)), 16: (setting16, (Game.WIDTH - 175, 380)), 20: (setting20, (Game.WIDTH - 175, 440)), 25: (setting25, (Game.WIDTH - 175, 500)), "pos": (120, 100)}
Game.remake_dict()

#Loading images and settings dictionary to Settings object.
Settings.set_img(settings_icon)
Settings.load_dict(SETTINGS_DICT)
Settings.set_sound_img(sound_on, sound_off)

#Screen, caption, icon, game variables and GUI settings.
screen = pygame.display.set_mode(Game.SIZE)
pygame.display.set_icon(icon)
pygame.display.set_caption(Game.CAPTION)
CLOCK = pygame.time.Clock()

#Music and sounds.
mixer.music.load(Game.FILES + r"/background.wav")
kill_sound = mixer.Sound(Game.FILES + r"/kill.wav")
winner_sound = mixer.Sound(Game.FILES + r"/game_winner.wav")
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
    pygame.draw.rect(screen, (125, 75, 255), (Game.WIDTH - 200, 0, Game.WIDTH, Game.HEIGHT))
    if Game.TIMER[1] == 42:
        #Easter egg.
        stopwatch = font.render("TIME: foo 42", True, black)
    else:
        stopwatch = font.render(f"TIME: {Game.TIMER[1]}", True, black)
    screen.blit(stopwatch, (Game.WIDTH - 175, 50))
    screen.blit(space_text, (Game.WIDTH - 175, 226))
    screen.blit(restart_text, (Game.WIDTH - 175, 258))
    screen.blit(rmb_text, (Game.WIDTH - 175, 353))
    screen.blit(flag_text, (Game.WIDTH - 175, 385))
    screen.blit(enter_text, (Game.WIDTH - 175, 480))
    screen.blit(reveal_text, (Game.WIDTH - 175, 512))


#Game loop.
Game.restart()

running = True
while running:
    CLOCK.tick(Game.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Game.restart()
            elif event.key == pygame.K_RETURN:
                Game.REVEALED = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

            s = screen.blit(Settings.img, (Game.WIDTH - Settings.x_left, Settings.y))
            if s.collidepoint(position):
                if event.button == 1:
                    Settings.is_open = not Settings.is_open
            
            if Settings.is_open:
                for d, text in zip(Settings.dictionary.items(), [text_9x9, text_11x11, text_13x13, text_16x16, text_20x20, text_25x25, None]):
                    if d[0] != "pos":
                        g = screen.blit(text, (d[1][1][0], d[1][1][1]))
                        if g.collidepoint(position):
                            if event.button == 1:
                                Settings = Settings.make()
                                Settings.__init__(d[0])
                                Game = Game.make()
                                Game.__init__()
                                Game.remake_dict()
                                Game.restart()
                
                i = screen.blit(sound_on, (Game.WIDTH - 100, 40))
                if i.collidepoint(position):
                    if event.button == 1:
                        Settings.is_sound = not Settings.is_sound
                        if Settings.is_sound:
                            mixer.music.play(-1)
                        else:
                            mixer.music.stop()

            if not Game.GAME_STOP and not Settings.is_open:
                for cell in Game.list_of_cells:
                    b = screen.blit(cell.img, (cell.x, cell.y))
                    if b.collidepoint(position):
                        if event.button == 1:
                            if not Game.has_activated_timer:
                                Game.has_activated_timer = True
                            cell.check_cell()
                        elif event.button == 3:
                            cell.marked = not cell.marked

    if Settings.is_open:
        Settings.show(Game.WIDTH, Game.HEIGHT)
    else:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, Game.WIDTH, Game.HEIGHT))

        for cell in Game.list_of_cells:
            cell.blit()

        if Game.has_activated_timer:
            Game.timer()
        
        instructions()
        Settings.blit(Game.WIDTH)
        Game.reveal_all()
        Game.is_finished()
    pygame.display.update()

