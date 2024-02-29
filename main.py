from amado import Amado
from gui import GUI
from gui import MainMenu
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
        main_menu = MainMenu()

        while main_menu.update() != False:
            main_menu.render()

        selected_level = main_menu.selected_level
        
        game = Amado(levels.STARTS[selected_level], levels.GOALS[selected_level], 0, 0, 0)

        if selected_level == -1:
            pygame.quit()
            sys.exit()

        game_gui = GUI(game, selected_level)

        while game_gui.update() != False:
            game_gui.render()

    # Ensure a cleen exit
    pygame.quit()
    sys.exit()
