from amado import Amado
from gui import GUI
import algorithms
import levels
import pygame
import sys

if __name__ == "__main__":
    level = 0

    game = Amado(levels.STARTS[level], levels.GOALS[level], 0, 0, 0)

    debug = False

    if debug:
        algorithms.breadth_first_search(game)
    else:
        gui = GUI(game, level)

        while gui.update() != False:
            gui.render()

    # Ensure a cleen exit
    pygame.quit()
    sys.exit()
