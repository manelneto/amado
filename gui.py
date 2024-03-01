from amado import Amado 
import algorithms
import levels
import pygame

class BaseGameScreen:
    def __init__(self, screen_width: int = 1200, screen_height: int = 800, change_state_callback=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.change_state_callback = change_state_callback
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont('Arial', 45)
        self.background_color = (0, 0, 0)
        pygame.display.set_caption('Amado Game')

    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def render(self):
        self.screen.fill(self.background_color)
        pygame.display.flip()

    # game_board -> True to highlight the selected cell, False otherwise
    def draw_board(self, pos_x, pos_y, board, scale, game_board = False):
        board_size = len(board)
        cell_size = self.cell_size * scale
        left_x = pos_x
        top_y = pos_y

        for y in range(board_size):
            for x in range(board_size):
                rect = pygame.Rect(left_x + x*cell_size, top_y + y*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, self.colors[board[y][x]], rect)
                if game_board and self.game_state and y == self.game_state.row and x == self.game_state.col:
                    pygame.draw.rect(self.screen, self.highlight_color, rect, 5)


class GUI(BaseGameScreen):
    def __init__(self, game_state: Amado, level: int, change_state_callback):
        super().__init__()
        self.change_state_callback = change_state_callback
        self.game_state = game_state
        self.level = level
        self.cell_size = 75
        self.colors = {'r': (255, 0, 0), 'y': (255, 216, 0), 'b': (0, 0, 255), 'n': (0, 0, 0)}
        self.highlight_color = (57, 255, 20)

    def draw_level_info(self):
        # draw current level
        counter_surface = self.font.render("Level " + str(self.level + 1), True, (0, 255, 0))
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
                elif event.key == pygame.K_ESCAPE:
                    if self.change_state_callback:
                        self.change_state_callback('menu')
                    return False
                elif event.key == pygame.K_q:
                    return False
        return True

    def render(self):
        self.screen.fill(self.background_color)

        # Draw play board
        board_x = int(self.screen_width / 3 - (len(self.game_state.board) * self.cell_size) / 2)
        board_y = int(self.screen_height / 2 - (len(self.game_state.board) * self.cell_size) / 2)
        self.draw_board(board_x, board_y, self.game_state.board, 1, True)

        # Draw goal board
        goal_board_cell_size = int(self.cell_size / 2)
        scale = goal_board_cell_size / self.cell_size
        left_x = self.screen_width - 150 - (len(self.game_state.goal_board) * goal_board_cell_size) / 2
        top_y = (len(self.game_state.goal_board) * goal_board_cell_size) / 2
        self.draw_board(left_x, top_y, self.game_state.goal_board, scale)

        # Draw extra info
        self.draw_goal()
        self.draw_level_info()

        # Update the screen
        pygame.display.flip()

class MainMenu(BaseGameScreen):
    def __init__(self, change_state_callback):
        super().__init__()
        self.change_state_callback = change_state_callback
        self.selected_level = 0 # Index of the currently selected level
        self.total_levels = len(levels.STARTS)
        self.level_cols = 5  # Number of columns to display levels

    def draw_main_menu(self):
        # Title
        title_font = pygame.font.SysFont('Arial', 90)
        title_surface = title_font.render("Amado", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width / 2, 50 + title_surface.get_height() / 2))

        self.screen.blit(title_surface, title_rect)

        # Draw levels
        self.draw_levels_menu()

    def draw_levels_menu(self):
        margin = 50
        content_height = self.screen_height - (margin * 2) - 100
        level_font = pygame.font.SysFont('Arial', 30)
        rows = (self.total_levels + self.level_cols - 1) // self.level_cols
        row_height = content_height / rows
        col_width = (self.screen_width - (margin * 2)) / self.level_cols

        for i in range(self.total_levels):
            col = i % self.level_cols
            row = i // self.level_cols
            level_text = f"Level {i + 1}"
            level_surface = level_font.render(level_text, True, (255, 255, 255))

            # Color green for selected level
            if i == self.selected_level:
                level_surface = level_font.render(level_text, True, (0, 255, 0))

            level_rect = level_surface.get_rect(center=((col * col_width) + col_width / 2 + margin, 
                                                        (row * row_height) + row_height / 2 + 100))

            self.screen.blit(level_surface, level_rect)

    def update(self) -> bool:
        # Should return False if the loop should stop
        # And True otherwise
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.selected_level = -1
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_level = (self.selected_level - self.level_cols) % self.total_levels
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_level = (self.selected_level + self.level_cols) % self.total_levels
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.selected_level = (self.selected_level - 1) % self.total_levels
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.selected_level = (self.selected_level + 1) % self.total_levels
                elif event.key == pygame.K_RETURN:
                    if self.change_state_callback:
                        self.change_state_callback('game', self.selected_level)
                    return False
                elif event.key == pygame.K_q:
                    # self.selected_level = -1
                    return False
                
        return True

    def render(self):
        self.screen.fill(self.background_color)
        self.draw_main_menu()
        pygame.display.flip()