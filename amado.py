import pygame
import sys
import levels

class Amado:
    def __init__(self, level: int):
        self.level = level

        self.board = levels.STARTS[self.level]
        self.board_size = len(self.board)
        self.goal_board = levels.GOALS[self.level]
        self.move_counter = 0

        self.colors = {'r', 'y', 'b'}
        self.row, self.col = 0, 0

        # pygame screen
        self.cell_size = 75
        self.screen_width = 1200
        self.screen_height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 45)

        # Colors
        self.background_color = (0, 0, 0)
        self.colors = {
            'r': (255, 0, 0),
            'y': (255, 255, 0),
            'b': (0, 0, 255),
        }
        self.highlight_color = (0, 255, 0)

        pygame.display.set_caption('Amado Game')

    def draw_board(self):
        left_x = int(self.screen_width / 3 - (self.board_size * self.cell_size) / 2)
        top_y = int(self.screen_height / 2 - (self.board_size * self.cell_size) / 2)

        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(left_x + x*self.cell_size,top_y + y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.colors[self.board[y][x]], rect)
                if y == self.row and x == self.col:
                    pygame.draw.rect(self.screen, self.highlight_color, rect, 5)  # Highlight the current cell

    def draw_goal(self):
        # draw the red line
        pygame.draw.line(self.screen, self.colors['r'], (self.screen_width - 300, 0), (self.screen_width - 300, self.screen_height), 5)

        # draw the goal board
        goal_board_cell_size = int(self.cell_size / 2)
        left_x = self.screen_width - 150 - (self.board_size * goal_board_cell_size) / 2
        top_y = (self.board_size * goal_board_cell_size) / 2

        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(left_x + x*goal_board_cell_size,top_y + y*goal_board_cell_size, goal_board_cell_size, goal_board_cell_size)
                pygame.draw.rect(self.screen, self.colors[self.goal_board[y][x]], rect)

    def draw_level_info(self):
        # draw current level
        counter_surface = self.font.render("Level " + str(self.level), True, (0, 255, 0))
        counter_position = (10, 20)
        self.screen.blit(counter_surface, counter_position)

        # draw move counter
        counter_surface = self.font.render(str(self.move_counter), True, (255, 255, 255))
        counter_position = (int(self.screen_width / 3), 20)
        self.screen.blit(counter_surface, counter_position)

    def update(self) -> bool:
        # Should return False if the game loop should stop
        # And True otherwise
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.up()
                elif event.key == pygame.K_s:
                    game.down()
                elif event.key == pygame.K_a:
                    game.left()
                elif event.key == pygame.K_d:
                    game.right()
                elif event.key == pygame.K_q:
                    return False
                
        return True

    def move(self, row: int , col: int):
        color1 = self.board[self.row][self.col]
        color2 = self.board[row][col]
        if color1 != color2:
            self.board[row][col] = self.swap(color1, color2)
        (self.row, self.col) = (row, col)

        self.move_counter += 1
        self.change_level()

    def swap(self, color1, color2):
        color_keys = set(self.colors.keys())
        color3 = color_keys - {color1, color2}
        return color3.pop()
    
    def up(self):
        if self.row > 0:
            self.move(self.row - 1, self.col)

    def down(self):
        if self.row < self.board_size - 1:
            self.move(self.row + 1, self.col)

    def left(self):
        if self.col > 0:
            self.move(self.row, self.col - 1)

    def right(self):
        if self.col < self.board_size - 1:
            self.move(self.row, self.col + 1)

    def render(self):
        game.screen.fill(game.background_color)
        game.draw_board()
        game.draw_goal()
        game.draw_level_info()
        pygame.display.flip()

    def change_level(self):
        if self.board == self.goal_board:
            self.level += 1

            if self.level < 10:
                self.board = levels.STARTS[self.level] 
                self.board_size = len(self.board)  
                self.goal_board = levels.GOALS[self.level]  
                self.move_counter = 0 
                self.row, self.col = 0, 0

            else:
                # Victory -> we might show a victory screen in the future
                print("Congratulations! You've completed all levels.")

if __name__ == "__main__":

    game = Amado(1)

    running = True
    while running:
        running = game.update()
        game.render()

    # Ensure a cleen exit
    pygame.quit()
    sys.exit()