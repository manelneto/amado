import pygame
import sys

class Amado:
    def __init__(self, board):
        self.board = board
        self.board_size = len(board)
        self.colors = {'r', 'y', 'b'}
        self.row, self.col = 0, 0

        # pygame screen
        self.cell_size = 100
        self.screen_width = self.board_size * self.cell_size
        self.screen_height = self.board_size * self.cell_size
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Initialize Pygame
        pygame.init()

        # Colors
        self.background_color = (255, 255, 255)
        self.colors = {
            'r': (255, 0, 0),
            'y': (255, 255, 0),
            'b': (0, 0, 255),
        }
        self.highlight_color = (0, 255, 0)

        pygame.display.set_caption('Amado Game')

    def draw_board(self):
        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.colors[self.board[y][x]], rect)
                if y == self.row and x == self.col:
                    pygame.draw.rect(self.screen, self.highlight_color, rect, 5)  # Highlight the current cell

    def move(self, row, col):
        color1 = self.board[self.row][self.col]
        color2 = self.board[row][col]
        if color1 != color2:
            self.board[row][col] = self.swap(color1, color2)
        (self.row, self.col) = (row, col)

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


if __name__ == "__main__":

    board = [
        ['y', 'y', 'y', 'b'],
        ['r', 'r', 'b', 'b'],
        ['r', 'b', 'b', 'b'],
        ['y', 'b', 'y', 'r'],
    ]

    game = Amado(board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                    running = False

        game.screen.fill(game.background_color)
        game.draw_board()
        pygame.display.flip()

    pygame.quit()
    sys.exit()