from amado import Amado 
import algorithms
import pygame

class BaseGameScreen:
    def __init__(self, screen_width: int = 1200, screen_height: int = 800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont('Arial', 45)
        self.background_color = (0, 0, 0)
        pygame.display.set_caption('Amado Game')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def render(self):
        self.screen.fill(self.background_color)
        pygame.display.flip()

class GUI(BaseGameScreen):
    def __init__(self, game_state: Amado, level: int):
        super().__init__()
        self.game_state = game_state
        self.level = level
        self.cell_size = 75
        self.colors = {'r': (255, 0, 0), 'y': (255, 216, 0), 'b': (0, 0, 255), 'n': (0, 0, 0)}
        self.highlight_color = (57, 255, 20)

    def draw_board(self):
        board_size = self.game_state.board_size
        left_x = int(self.screen_width / 3 - (board_size * self.cell_size) / 2)
        top_y = int(self.screen_height / 2 - (board_size * self.cell_size) / 2)

        for y in range(board_size):
            for x in range(board_size):
                rect = pygame.Rect(left_x + x*self.cell_size, top_y + y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.colors[self.game_state.board[y][x]], rect)
                if y == self.game_state.row and x == self.game_state.col:
                    pygame.draw.rect(self.screen, self.highlight_color, rect, 5)

    def draw_goal(self):
        board_size = self.game_state.board_size
        pygame.draw.line(self.screen, self.colors['r'], (self.screen_width - 300, 0), (self.screen_width - 300, self.screen_height), 5)
        goal_board_cell_size = int(self.cell_size / 2)
        left_x = self.screen_width - 150 - (board_size * goal_board_cell_size) / 2
        top_y = (board_size * goal_board_cell_size) / 2

        for y in range(board_size):
            for x in range(board_size):
                rect = pygame.Rect(left_x + x*goal_board_cell_size, top_y + y*goal_board_cell_size, goal_board_cell_size, goal_board_cell_size)
                pygame.draw.rect(self.screen, self.colors[self.game_state.goal_board[y][x]], rect)

    def draw_level_info(self):
        level_surface = self.font.render(f"Level {self.level}", True, (0, 255, 0))
        self.screen.blit(level_surface, (10, 20))

        move_counter_surface = self.font.render(str(self.game_state.move_counter), True, (255, 255, 255))
        self.screen.blit(move_counter_surface, (self.screen_width / 3, 20))

    def update(self):
        if not self.handle_events():
            return False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.game_state = algorithms.up(self.game_state)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.game_state = algorithms.down(self.game_state)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.game_state = algorithms.left(self.game_state)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.game_state = algorithms.right(self.game_state)
                elif event.key == pygame.K_q:
                    return False
        return True

    def render(self):
        super().render()
        self.draw_board()
        self.draw_goal()
        self.draw_level_info()
        pygame.display.flip()

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

class MainMenu(BaseGameScreen):
    def __init__(self):
        super().__init__()