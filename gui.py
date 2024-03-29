from amado import Amado 
import algorithms
import levels
import pygame
import time


class BaseGameScreen:
    def __init__(self, screen_width: int = 1200, screen_height: int = 750, change_state_callback = None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.change_state_callback = change_state_callback
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont('Arial', 45)
        self.background_color = (0, 0, 0)
        self.game_cell_size = 75
        self.colors = {'r': (255, 0, 0), 'y': (255, 216, 0), 'b': (0, 0, 255), 'n': (0, 0, 0)}
        self.highlight_color = (57, 255, 20)
        pygame.display.set_caption('Amado Game')

    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def render(self):
        self.screen.fill(self.background_color)
        pygame.display.flip()

    def draw_board(self, pos_x: int, pos_y: int, board: list, scale: int, highlight: bool = False):
        board_size = len(board)
        cell_size = self.game_cell_size * scale

        for y in range(board_size):
            for x in range(board_size):
                rect = pygame.Rect(pos_x + x * cell_size, pos_y + y * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.screen, self.colors[board[y][x]], rect)
                if highlight and self.game_state and y == self.game_state.row and x == self.game_state.col:
                    pygame.draw.rect(self.screen, self.highlight_color, rect, 5)


class GUI(BaseGameScreen):
    def __init__(self, game_state: Amado, level: int, change_state_callback):
        super().__init__()
        self.change_state_callback = change_state_callback
        self.game_state = game_state
        self.level = level
        self.move_counter = 0
        self.goal_board = levels.GOALS[level]
        
        self.hint_message = None
        
        self.bot_playing = False
        self.bot_plays = []
        self.bot_play_index = 0
        
        self.algorithm_menu = False
        self.button_rect = {}
        self.algorithms = [
            {"name": "Breadth First Search", "key": "bfs", "position": (930, 250)},
            {"name": "Depth First Search", "key": "dfs", "position": (930, 300)},
            {"name": "Depth Limited Search", "key": "dls", "position": (930, 350)},
            {"name": "Iterative Deepening Search", "key": "ids", "position": (930, 400)},
            {"name": "Greedy Search", "key": "gs", "position": (930, 450)},
            {"name": "A* Search", "key": "astar", "position": (930, 500)},
            {"name": "Weighted A* Search", "key": "wastar", "position": (930, 550)}
        ]

    def show_hint(self):
        hint_path = algorithms.greedy_search(self.game_state, self.goal_board)
        if hint_path and len(hint_path) > 1:
            next_state = hint_path[1] 
            direction = self.determine_direction(self.game_state, next_state)
            self.hint_message = f"Go {direction}"

    def determine_direction(self, current_state: Amado, next_state: Amado):
        row_diff = next_state.row - current_state.row
        col_diff = next_state.col - current_state.col
        if row_diff == -1:
            return "up"
        elif row_diff == 1:
            return "down"
        elif col_diff == -1:
            return "left"
        elif col_diff == 1:
            return "right"
        return "any valid direction"

    def draw_algorithm_menu(self):
        self.algorithm_menu = True
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Auto Run
        auto_run = pygame.font.SysFont('Arial', 25).render("Auto Run", True, (255, 255, 255))
        auto_run_pos = (self.screen_width * 0.83, self.screen_height * 0.8)
        auto_run_rect = auto_run.get_rect(topleft = auto_run_pos)
        self.screen.blit(auto_run, auto_run_pos)
        self.button_rect["auto_run"] = auto_run_rect
        
        if auto_run_rect.collidepoint(mouse_x, mouse_y):
            auto_run = pygame.font.SysFont('Arial', 25).render("Auto Run", True, (57, 255, 20))
            self.screen.blit(auto_run, auto_run_pos)

        # Exit Algorithm
        exit_button = pygame.font.SysFont('Arial', 25).render("Exit Algorithm", True, (255, 255, 255))
        exit_pos = (self.screen_width * 0.81, self.screen_height * 0.85)
        exit_rect = exit_button.get_rect(topleft = exit_pos)
        self.screen.blit(exit_button, exit_pos)
        self.button_rect["exit_button"] = exit_rect

        if exit_rect.collidepoint(mouse_x, mouse_y):
            exit_button = pygame.font.SysFont('Arial', 25).render("Exit Algorithm", True, (255, 0, 0))
            self.screen.blit(exit_button, exit_pos)

        # Right Arrow
        arrow_right = pygame.font.SysFont('Arial', 50).render(">", True, (255, 255, 255))
        arrow_right_pos = (self.screen_width * 0.90, self.screen_height * 0.70)
        arrow_right_rect = arrow_right.get_rect(topleft = arrow_right_pos)
        self.screen.blit(arrow_right, arrow_right_pos)
        self.button_rect["arrow_right"] = arrow_right_rect

        if arrow_right_rect.collidepoint(mouse_x, mouse_y):
            arrow_right = pygame.font.SysFont('Arial', 50).render(">", True, (57, 255, 20))
            self.screen.blit(arrow_right, arrow_right_pos)

        # Left Arrow
        arrow_left = pygame.font.SysFont('Arial', 50).render("<", True, (255, 255, 255))
        arrow_left_pos = (self.screen_width * 0.82, self.screen_height * 0.70)
        arrow_left_rect = arrow_left.get_rect(topleft = arrow_left_pos)
        self.screen.blit(arrow_left, arrow_left_pos)
        self.button_rect["arrow_left"] = arrow_left_rect

        if arrow_left_rect.collidepoint(mouse_x, mouse_y):
            arrow_left = pygame.font.SysFont('Arial', 50).render("<", True, (57, 255, 20))
            self.screen.blit(arrow_left, arrow_left_pos)

    def draw_algorithms(self):
        self.algorithm_menu = False
        
        for algorithm in self.algorithms:
            self.draw_algorithm_button(algorithm, algorithm['position'])

    def draw_hint(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        hint_font = pygame.font.SysFont('Arial', 25)
        hint_button = hint_font.render("Hint", True, (255, 255, 255))
        hint_button_width, hint_button_height = hint_button.get_size()
        hint_button_pos = (self.screen_width / 2 + 430, self.screen_height - hint_button_height - 50)
        hint_button_rect = hint_button.get_rect(topleft = hint_button_pos)
        self.screen.blit(hint_button, hint_button_pos)
        self.button_rect["hint"] = hint_button_rect

        if hint_button_rect.collidepoint(mouse_x, mouse_y) or self.hint_message:
            hint_button = hint_font.render("Hint", True, (57, 255, 20))
            self.screen.blit(hint_button, hint_button_pos)

        if self.hint_message:
            hint_msg_pos = (self.screen_width / 2 + 415, self.screen_height - hint_button_height - 20)
            hint_msg = hint_font.render(self.hint_message, True, (255, 255, 255))
            self.screen.blit(hint_msg, hint_msg_pos)

    def draw_algorithm_button(self, algorithm: dict, position: tuple):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        default_color = (255, 255, 255)
        hover_color = (57, 255, 20)
        
        algo_surface = pygame.font.SysFont('Arial', 25).render(algorithm['name'], True, default_color)
        algo_rect = algo_surface.get_rect(topleft=position)
        
        # If mouse hovers over the button, change the color
        if algo_rect.collidepoint(mouse_x, mouse_y):
            algo_surface = pygame.font.SysFont('Arial', 25).render(algorithm['name'], True, hover_color)
        
        self.screen.blit(algo_surface, position)
        self.button_rect[algorithm['key']] = algo_rect  # Store the button rect for click detection

    def draw_level_info(self):
        # Red Line
        pygame.draw.line(self.screen, self.colors['r'], (self.screen_width - 300, 0), (self.screen_width - 300, self.screen_height), 5)
        
        # Level N
        counter_surface = self.font.render("Level " + str(self.level), True, self.highlight_color)
        counter_position = (10, 20)
        self.screen.blit(counter_surface, counter_position)

        # Move Counter
        counter_surface = self.font.render(str(self.move_counter), True, (255, 255, 255))
        counter_position = (int(self.screen_width / 3), 20)
        self.screen.blit(counter_surface, counter_position)

        # Press ESC for Menu
        counter_surface = pygame.font.SysFont('Arial', 25).render("Press ESC for Menu" , True, (255, 255, 255))
        counter_position = (10, self.screen_height - 30)
        self.screen.blit(counter_surface, counter_position)

    # Returns False if the game loop should stop, and True otherwise
    def update(self) -> bool:
        if algorithms.goal_test(self.game_state, self.goal_board):
            time.sleep(0.5)
            self.change_state_callback('win', self.level, self.move_counter)
            return True

        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_game_state = self.game_state

        if self.bot_playing:
            self.bot_play_index += 1
            new_game_state = self.bot_plays[self.bot_play_index]
            time.sleep(1)
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.algorithm_menu:
                        if self.button_rect.get("auto_run") and self.button_rect["auto_run"].collidepoint(mouse_x, mouse_y):
                            self.bot_playing = True
                        elif self.button_rect.get("exit_button") and self.button_rect["exit_button"].collidepoint(mouse_x, mouse_y):
                            self.bot_play_index = 0
                            self.bot_plays = []
                        elif self.button_rect.get("arrow_right") and self.button_rect["arrow_right"].collidepoint(mouse_x, mouse_y):
                            self.bot_play_index += 1
                            new_game_state = self.bot_plays[self.bot_play_index]
                        elif self.move_counter > 0 and self.button_rect.get("arrow_left") and self.button_rect["arrow_left"].collidepoint(mouse_x, mouse_y):
                            self.bot_play_index -= 1
                            self.move_counter -= 2
                            new_game_state = self.bot_plays[self.bot_play_index]
                    else:
                        if self.button_rect.get("bfs") and self.button_rect["bfs"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.breadth_first_search(self.game_state, self.goal_board)
                        elif self.button_rect.get("dfs") and self.button_rect["dfs"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.depth_first_search(self.game_state, self.goal_board)
                        elif self.button_rect.get("dls") and self.button_rect["dls"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.depth_limited_search(self.game_state, self.goal_board)
                        elif self.button_rect.get("ids") and self.button_rect["ids"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.iterative_deepening_search(self.game_state, self.goal_board)
                        elif self.button_rect.get("gs") and self.button_rect["gs"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.greedy_search(self.game_state, self.goal_board)
                        elif self.button_rect.get("astar") and self.button_rect["astar"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.a_star(self.game_state, self.goal_board)
                        elif self.button_rect.get("wastar") and self.button_rect["wastar"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = algorithms.a_star(self.game_state, self.goal_board, 1.5)
                        elif self.button_rect.get("hint") and self.button_rect["hint"].collidepoint(mouse_x, mouse_y):
                            self.show_hint()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        new_game_state = algorithms.up(self.game_state)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        new_game_state = algorithms.down(self.game_state)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        new_game_state = algorithms.left(self.game_state)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        new_game_state = algorithms.right(self.game_state)
                    elif event.key == pygame.K_ESCAPE:
                        if self.change_state_callback:
                            self.change_state_callback('menu')
                        return False
                    elif event.key == pygame.K_q:
                        return False

        if new_game_state != self.game_state:
            self.hint_message = None
            self.game_state = new_game_state
            self.move_counter += 1

        return True

    def render(self):
        self.screen.fill(self.background_color)

        # Game Board
        board_x = int(self.screen_width / 3 - (len(self.game_state.board) * self.game_cell_size) / 2)
        board_y = int(self.screen_height / 2 - (len(self.game_state.board) * self.game_cell_size) / 2)
        self.draw_board(board_x, board_y, self.game_state.board, 1, True)

        # Goal Board
        goal_board_cell_size = int(self.game_cell_size / 2)

        if self.level >= 7 and self.level <= 9:
            goal_board_cell_size /= 1.2
        if self.level == 10:
            goal_board_cell_size /= 1.7

        scale = goal_board_cell_size / self.game_cell_size

        left_x = self.screen_width - 150 - (len(self.goal_board) * goal_board_cell_size) / 2
        top_y = 50
        self.draw_board(left_x, top_y, self.goal_board, scale)

        # Side Menu
        if self.bot_plays:
            self.draw_algorithm_menu()
        else:
            self.draw_algorithms()
            self.draw_hint()

        # Level Info
        self.draw_level_info()

        pygame.display.flip()


class MainMenu(BaseGameScreen):
    def __init__(self, change_state_callback):
        super().__init__()
        self.change_state_callback = change_state_callback
        self.selected_level = 1
        self.total_levels = len(levels.STARTS)
        self.level_cols = 5

    def draw_main_menu(self):
        # Title
        title_font = pygame.font.SysFont('Arial', 90)
        title_surface = title_font.render("Amado", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width / 2, 50 + title_surface.get_height() / 2))

        self.screen.blit(title_surface, title_rect)

        # Levels
        self.draw_levels_menu()

    def draw_levels_menu(self):
        margin = 50
        top_margin_offset = 250
        content_height = self.screen_height - (margin * 2) - top_margin_offset
        level_font = pygame.font.SysFont('Arial', 30)
        rows = (self.total_levels + self.level_cols - 1) // self.level_cols
        row_height = content_height / rows
        col_width = (self.screen_width - (margin * 2)) / self.level_cols

        for i in range(1, self.total_levels + 1):
            col = (i - 1) % self.level_cols
            row = (i - 1) // self.level_cols
            level_text = f"Level {i}"
            level_surface = level_font.render(level_text, True, (255, 255, 255))

            # Highlight selected level
            if i == self.selected_level:
                level_surface = level_font.render(level_text, True, (0, 255, 0))

            # Draw level number
            text_x = (col * col_width) + col_width / 2 + margin
            text_y = (row * row_height) + top_margin_offset
            level_rect = level_surface.get_rect(center=(text_x, text_y))
            self.screen.blit(level_surface, level_rect)

            # Draw level board
            level_board = levels.GOALS[i]
            mini_board_width = len(level_board[0]) * self.game_cell_size * 0.1
            mini_board_pos_x = text_x - mini_board_width / 2 - 10
            mini_board_pos_y = text_y + level_surface.get_height() / 2 + 15
            mini_board_scale = 0.15
            self.draw_board(mini_board_pos_x, mini_board_pos_y, level_board, mini_board_scale)

    # Returns False if the game loop should stop, and True otherwise
    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_level = max(1, (self.selected_level - self.level_cols - 1) % self.total_levels + 1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_level = min(self.total_levels, (self.selected_level + self.level_cols - 1) % self.total_levels + 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.selected_level > 1:
                        self.selected_level -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.selected_level < self.total_levels:
                        self.selected_level += 1
                elif event.key == pygame.K_RETURN:
                    if self.change_state_callback:
                        self.change_state_callback('game', self.selected_level)
                    return False
                elif event.key == pygame.K_q:
                    return False

        return True

    def render(self):
        self.screen.fill(self.background_color)
        self.draw_main_menu()
        pygame.display.flip()


class WinMenu(BaseGameScreen):
    def __init__(self, level: int, score: int, change_state_callback):
        super().__init__()
        self.change_state_callback = change_state_callback
        self.level = level
        self.score = score

    def draw_win_menu(self):
        # Level X Completed
        level_completed = pygame.font.SysFont('Arial', 75).render(f"Level {self.level} Completed!", True, (57, 255, 20))
        level_completed_pos = (self.screen_width / 2 - level_completed.get_width() / 2, 150)
        self.screen.blit(level_completed, level_completed_pos)

        # Score = X
        score_text = pygame.font.SysFont('Arial', 50).render(f"Score = {self.score} ", True, (255, 255, 255))
        score_text_pos = (self.screen_width / 2 - score_text.get_width() / 2, 300)
        self.screen.blit(score_text, score_text_pos)

        # Press ESC for Menu"
        counter_surface = pygame.font.SysFont('Arial', 25).render("Press ESC for Menu" , True, (255, 255, 255))
        counter_position = (10, self.screen_height - 30)
        self.screen.blit(counter_surface, counter_position)

    # Returns False if the game loop should stop, and True otherwise
    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    self.change_state_callback('menu')
                elif event.key == pygame.K_q:
                    return False

        return True
    
    def render(self):
        self.screen.fill(self.background_color)
        self.draw_win_menu()
        pygame.display.flip()
