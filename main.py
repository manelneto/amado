from amado import Amado
from gui import GUI
from gui import MainMenu
import algorithms
import levels
import pygame
import sys

def change_state(new_state, level=0):
    debug = True

    if new_state == 'menu':
        current_screen = MainMenu(change_state_callback=change_state)
    elif new_state == 'game':
        game_state = Amado(levels.STARTS[level], levels.GOALS[level], 0, 0, 0)
        if debug:
            algorithms.breadth_first_search(game_state)
            return
        else:
            current_screen = GUI(game_state, level, change_state_callback=change_state)
    while current_screen.update():
        current_screen.render()

if __name__ == "__main__":
    change_state('menu')
