# **Minesweeper**

Implementation of Minesweeper in python using module pygame.

---

## **Requirements**

- **Python 3.7.7** or greater: Visit [python's website](https://www.python.org/ "Go to the website").
- **Pygame**: Use `pip install pygame` or visit [pygame's website](https://www.pygame.org/wiki/GettingStarted "Go to the website").

---

## **How to use**

### **How to run**

1. Download the repository.
2. Make sure your software meets the requirements.
3. Open the terminal.
4. Run *minesweeper .py* with python 3.7.7 or greater.

### **How to play**

Player has to reveal all the cells excluding the mines.\
The game ends if player either:
- clicks on the mine,
- reveals all the cells that are not mines,
- reveals all the mines using special input.

Control panel is located on the right side of the screen.\
To enter / exit settings' menu, player has to click on the settings wheel.

![Settings wheel](settings_icon.png)

Inside settings' menu, player can:
- turn music on / off,
- select the size of the grid (Default: 9 x 9).

### **Controls**

- Left mouse button (LMB)
    - Main input, used to reveal the clicked cell or to enter settings' menu.

- Right mouse button (RMB)
    - Used to flag the clicked cell (if the user thinks it might be a mine).

- Enter / Return
    - Used to reveal all the mines.

- Spacebar
    - Used to restart the game.