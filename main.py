from amado import Amado
from gui import GUI
from gui import MainMenu
import levels

def change_state(new_state, level=0):
    if new_state == 'menu':
        current_screen = MainMenu(change_state_callback=change_state)
    elif new_state == 'game':
        game_state = Amado(levels.STARTS[level], 0, 0)
        current_screen = GUI(game_state, level, change_state_callback=change_state)
    while current_screen.update():
        current_screen.render()

if __name__ == "__main__":
    change_state('menu')
