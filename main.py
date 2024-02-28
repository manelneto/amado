from amado import Amado
from gui import GUI
import levels
import pygame
import sys

if __name__ == "__main__":
    level = 1

    game = Amado(levels.STARTS[level], levels.GOALS[level], 0, 0, 0)

    gui = GUI(game, level)

    while gui.update() != False:
        gui.render()

    # Ensure a cleen exit
    pygame.quit()
    sys.exit()
