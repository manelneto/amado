from amado import Amado 
import algorithms
import pygame

class GUI:
    def __init__(self, game_state: Amado, level: int):
        self.game_state = game_state
        self.level = level

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
            'y': (255, 216, 0),
            'b': (0, 0, 255),
            'n': (0, 0, 0),
        }
        self.highlight_color = (57, 255, 20)

        pygame.display.set_caption('Amado Game')

    def draw_board(self):
        board_size = self.game_state.board_size
        left_x = int(self.screen_width / 3 - (board_size * self.cell_size) / 2)
        top_y = int(self.screen_height / 2 - (board_size * self.cell_size) / 2)

        for y in range(board_size):
            for x in range(board_size):
                rect = pygame.Rect(left_x + x*self.cell_size,top_y + y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.colors[self.game_state.board[y][x]], rect)
                if y == self.game_state.row and x == self.game_state.col:
                    pygame.draw.rect(self.screen, self.highlight_color, rect, 5)  # Highlight the current cell

    def draw_goal(self):
        board_size = self.game_state.board_size
        # draw the red line
        pygame.draw.line(self.screen, self.colors['r'], (self.screen_width - 300, 0), (self.screen_width - 300, self.screen_height), 5)

        # draw the goal board
        goal_board_cell_size = int(self.cell_size / 2)
        left_x = self.screen_width - 150 - (board_size * goal_board_cell_size) / 2
        top_y = (board_size * goal_board_cell_size) / 2

        for y in range(board_size):
            for x in range(board_size):
                rect = pygame.Rect(left_x + x*goal_board_cell_size,top_y + y*goal_board_cell_size, goal_board_cell_size, goal_board_cell_size)
                pygame.draw.rect(self.screen, self.colors[self.game_state.goal_board[y][x]], rect)

    def draw_level_info(self):
        # draw current level
        counter_surface = self.font.render("Level " + str(self.level), True, (0, 255, 0))
        counter_position = (10, 20)
        self.screen.blit(counter_surface, counter_position)

        # draw move counter
        counter_surface = self.font.render(str(self.game_state.move_counter), True, (255, 255, 255))
        counter_position = (int(self.screen_width / 3), 20)
        self.screen.blit(counter_surface, counter_position)

    def update(self) -> bool:
        # Should return False if the game loop should stop
        # And True otherwise
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.game_state = algorithms.up(self.game_state)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.game_state = algorithms.down(self.game_state)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.game_state = algorithms.left(self.game_state)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.game_state = algorithms.right(self.game_state)
                elif event.key == pygame.K_q:
                    return False
        return True

    def render(self):
        self.screen.fill(self.background_color)
        self.draw_board()
        self.draw_goal()
        self.draw_level_info()
        pygame.display.flip()
