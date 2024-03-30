from amado import Amado
from gui import GUI
from gui import MainMenu
from gui import WinMenu
import levels
import pygame
import sys

def change_state(new_state: str, level: int = 0, score: int = 0):
    if new_state == "menu":
        current_screen = MainMenu(change_state_callback = change_state)
    elif new_state == "game":
        game_state = Amado(levels.STARTS[level], 0, 0)
        current_screen = GUI(game_state, level, change_state_callback = change_state)
    elif new_state == "win":
        current_screen = WinMenu(level, score, change_state_callback = change_state)
    
    while current_screen.update():
        current_screen.render()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    change_state("menu")
