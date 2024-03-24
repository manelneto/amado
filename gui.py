from amado import Amado 
import algorithms
import levels
import pygame
import sys
import time

class BaseGameScreen:
    def __init__(self, screen_width: int = 1200, screen_height: int = 750, change_state_callback=None):
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

    # game_board -> True to highlight the selected cell, False otherwise
    def draw_board(self, pos_x, pos_y, board, scale, game_board = False):
        board_size = len(board)
        cell_size = self.game_cell_size * scale
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
        self.move_counter = 0
        self.goal_board = levels.GOALS[level]
        
        # True if algorithm is running , False if player is playing
        self.bot_playing = False
        # List of plays to be made by the bot
        self.bot_plays = []
        # Index of current bot play
        self.bot_play_index = 0
        # Hash Map with buttons needed
        self.button_rect = {}
        # Either "algorithms" or "algorithm_menu"
        self.current_menu = ""

    def draw_level_info(self):
        # draw the red line
        pygame.draw.line(self.screen, self.colors['r'], (self.screen_width - 300, 0), (self.screen_width - 300, self.screen_height), 5)
        
        # draw current level
        counter_surface = self.font.render("Level " + str(self.level), True, self.highlight_color)
        counter_position = (10, 20)
        self.screen.blit(counter_surface, counter_position)

        # draw move counter
        counter_surface = self.font.render(str(self.move_counter), True, (255, 255, 255))
        counter_position = (int(self.screen_width / 3), 20)
        self.screen.blit(counter_surface, counter_position)

        # draw "ESC to get back"
        counter_surface = pygame.font.SysFont('Arial', 25).render("Press ESC for Menu" , True, (255, 255, 255))
        counter_position = (10, self.screen_height - 30)
        self.screen.blit(counter_surface, counter_position)

    def draw_algorithm_menu(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Auto Run
        auto_run = pygame.font.SysFont('Arial', 25).render("Auto Run", True, (255, 255, 255))
        auto_run_pos = (self.screen_width * 0.83, self.screen_height * 0.8)
        auto_run_rect = auto_run.get_rect(topleft=auto_run_pos)
        self.screen.blit(auto_run, auto_run_pos)
        self.button_rect["auto_run"] = auto_run_rect
        
        if auto_run_rect.collidepoint(mouse_x, mouse_y):
            auto_run = pygame.font.SysFont('Arial', 25).render("Auto Run", True, (57, 255, 20))
            self.screen.blit(auto_run, auto_run_pos)

        # Exit Algorithm
        exit_button = pygame.font.SysFont('Arial', 25).render("Exit Algorithm", True, (255, 255, 255))
        exit_pos = (self.screen_width * 0.81, self.screen_height * 0.85)
        exit_rect = exit_button.get_rect(topleft=exit_pos)
        self.screen.blit(exit_button, exit_pos)
        self.button_rect["exit_button"] = exit_rect

        if exit_rect.collidepoint(mouse_x, mouse_y):
            exit_button = pygame.font.SysFont('Arial', 25).render("Exit Algorithm", True, (255, 0, 0))
            self.screen.blit(exit_button, exit_pos)

        # Arrow right
        arrow_right = pygame.font.SysFont('Arial', 50).render(">", True, (255, 255, 255))
        arrow_right_pos = (self.screen_width * 0.90, self.screen_height * 0.70)
        arrow_right_rect = arrow_right.get_rect(topleft=arrow_right_pos)
        self.screen.blit(arrow_right, arrow_right_pos)
        self.button_rect["arrow_right"] = arrow_right_rect

        if arrow_right_rect.collidepoint(mouse_x, mouse_y):
            arrow_right = pygame.font.SysFont('Arial', 50).render(">", True, (57, 255, 20))
            self.screen.blit(arrow_right, arrow_right_pos)

        # Arrow left
        arrow_left = pygame.font.SysFont('Arial', 50).render("<", True, (255, 255, 255))
        arrow_left_pos = (self.screen_width * 0.82, self.screen_height * 0.70)
        arrow_left_rect = arrow_left.get_rect(topleft=arrow_left_pos)
        self.screen.blit(arrow_left, arrow_left_pos)
        self.button_rect["arrow_left"] = arrow_left_rect

        if arrow_left_rect.collidepoint(mouse_x, mouse_y):
            arrow_left = pygame.font.SysFont('Arial', 50).render("<", True, (57, 255, 20))
            self.screen.blit(arrow_left, arrow_left_pos)

    # Should return False if the game loop should sto and True otherwise
    def update(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_game_state = self.game_state

        if self.bot_playing:
            if self.bot_play_index - 1 != len(self.bot_plays):
                self.bot_play_index += 1
                new_game_state = self.bot_plays[self.bot_play_index]
                time.sleep(1)
            else:
                self.bot_playing = False
                self.bot_plays = []
                # Exit game for now because there is no winning condition yet
                pygame.quit()
                sys.exit()
                
        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_menu == "algorithm_menu":
                        if self.button_rect.get("auto_run") and self.button_rect["auto_run"].collidepoint(mouse_x, mouse_y):
                            self.bot_playing = True
                        elif self.button_rect.get("exit_button") and self.button_rect["exit_button"].collidepoint(mouse_x, mouse_y):
                            self.bot_plays = []
                        elif self.button_rect.get("arrow_right") and self.button_rect["arrow_right"].collidepoint(mouse_x, mouse_y):
                            self.bot_play_index += 1
                            new_game_state = self.bot_plays[self.bot_play_index]
                        elif self.move_counter > 0 and self.button_rect.get("arrow_left") and self.button_rect["arrow_left"].collidepoint(mouse_x, mouse_y):
                            self.bot_play_index -= 1
                            self.move_counter -= 2 # because 1 is added by default at end
                            new_game_state = self.bot_plays[self.bot_play_index]
                    else:
                        # select the algorithm
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
            self.game_state = new_game_state
            self.move_counter += 1

        if algorithms.goal_test(self.game_state, self.goal_board):
            self.change_state_callback('win', self.level, self.move_counter)

        return True

    def render(self):
        self.screen.fill(self.background_color)

        # Draw play board
        board_x = int(self.screen_width / 3 - (len(self.game_state.board) * self.game_cell_size) / 2)
        board_y = int(self.screen_height / 2 - (len(self.game_state.board) * self.game_cell_size) / 2)
        self.draw_board(board_x, board_y, self.game_state.board, 1, True)

        # Draw goal board
        goal_board_cell_size = int(self.game_cell_size / 2)

        if self.level >= 7 and self.level <= 9:
            goal_board_cell_size /= 1.2
        if self.level == 10:
            goal_board_cell_size /= 1.7

        scale = goal_board_cell_size / self.game_cell_size

        left_x = self.screen_width - 150 - (len(self.goal_board) * goal_board_cell_size) / 2
        top_y = 50
        self.draw_board(left_x, top_y, self.goal_board, scale)

        # Check if algorithm was selected
        if not self.bot_plays:
            self.current_menu = "algorithms"
            self.draw_algorithms()
        else:
            self.current_menu = "algorithm_menu"
            self.draw_algorithm_menu()

        # Draw extra info
        self.draw_level_info()

        # Update the screen
        pygame.display.flip()

    def draw_algorithms(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # draw BFS below current level
        bfs_surface = pygame.font.SysFont('Arial', 25).render("Breadth First Search", True, (255, 255, 255))
        bfs_position = (930, 250)
        bfs_rect = bfs_surface.get_rect(topleft=bfs_position)
        self.screen.blit(bfs_surface, bfs_position)
        self.button_rect["bfs"] = bfs_rect

        if bfs_rect.collidepoint(mouse_x, mouse_y):
            bfs_surface = pygame.font.SysFont('Arial', 25).render("Breadth First Search", True, (57, 255, 20))
            self.screen.blit(bfs_surface, bfs_position)

        # draw DFS below current level
        dfs_surface = pygame.font.SysFont('Arial', 25).render("Depth First Search", True, (255, 255, 255))
        dfs_position = (930, 300)
        dfs_rect = dfs_surface.get_rect(topleft=dfs_position)
        self.screen.blit(dfs_surface, dfs_position)
        self.button_rect["dfs"] = dfs_rect

        if dfs_rect.collidepoint(mouse_x, mouse_y):
            dfs_surface = pygame.font.SysFont('Arial', 25).render("Depth First Search", True, (57, 255, 20))
            self.screen.blit(dfs_surface, dfs_position)

        # draw DLS below current level
        dls_surface = pygame.font.SysFont('Arial', 25).render("Depth Limited Search", True, (255, 255, 255))
        dls_position = (930, 350)
        dls_rect = dls_surface.get_rect(topleft=dls_position)
        self.screen.blit(dls_surface, dls_position)
        self.button_rect["dls"] = dls_rect

        if dls_rect.collidepoint(mouse_x, mouse_y):
            dls_surface = pygame.font.SysFont('Arial', 25).render("Depth Limited Search", True, (57, 255, 20))
            self.screen.blit(dls_surface, dls_position)

        # draw IDS below current level
        ids_surface = pygame.font.SysFont('Arial', 25).render("Iterative Deepening Search", True, (255, 255, 255))
        ids_position = (930, 400)
        ids_rect = ids_surface.get_rect(topleft=ids_position)
        self.screen.blit(ids_surface, ids_position)
        self.button_rect["ids"] = ids_rect

        if ids_rect.collidepoint(mouse_x, mouse_y):
            ids_surface = pygame.font.SysFont('Arial', 25).render("Iterative Deepening Search", True, (57, 255, 20))
            self.screen.blit(ids_surface, ids_position)

        # draw GS below current level
        gs_surface = pygame.font.SysFont('Arial', 25).render("Greedy Search", True, (255, 255, 255))
        gs_position = (930, 450)
        gs_rect = gs_surface.get_rect(topleft=gs_position)
        self.screen.blit(gs_surface, gs_position)
        self.button_rect["gs"] = gs_rect

        if gs_rect.collidepoint(mouse_x, mouse_y):
            gs_surface = pygame.font.SysFont('Arial', 25).render("Greedy Search", True, (57, 255, 20))
            self.screen.blit(gs_surface, gs_position)

class MainMenu(BaseGameScreen):
    def __init__(self, change_state_callback):
        super().__init__()
        self.change_state_callback = change_state_callback
        self.selected_level = 1 # Index of the currently selected level
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

            # Color green for selected level
            if i == self.selected_level:
                level_surface = level_font.render(level_text, True, (0, 255, 0))

            # Calculate the position for the text
            text_x = (col * col_width) + col_width / 2 + margin
            text_y = (row * row_height) + top_margin_offset
            level_rect = level_surface.get_rect(center=(text_x, text_y))

            # Draw the level number
            self.screen.blit(level_surface, level_rect)

            # Retrieve the board for the current level
            level_board = levels.GOALS[i]

            # Calculate the width of the mini board
            mini_board_width = len(level_board[0]) * self.game_cell_size * 0.1

            # Calculate the position for the mini board below the level text, centered
            mini_board_pos_x = text_x - mini_board_width / 2 - 10
            mini_board_pos_y = text_y + level_surface.get_height() / 2 + 15   # Spacing below the level number text

            # Draw the mini board representation
            mini_board_scale = 0.15
            self.draw_board(mini_board_pos_x, mini_board_pos_y, level_board, mini_board_scale)


    def update(self) -> bool:
        # Should return False if the loop should stop
        # And True otherwise
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

        # draw "ESC to get back"
        counter_surface = pygame.font.SysFont('Arial', 25).render("Press ESC for Menu" , True, (255, 255, 255))
        counter_position = (10, self.screen_height - 30)
        self.screen.blit(counter_surface, counter_position)

    def update(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # if user presses key, go back to main menu
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
