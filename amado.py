class Amado:
    def __init__(self, board: list, goal_board: list, move_counter: int, row: int, col: int):
        self.board = board
        self.goal_board = goal_board
        self.move_counter = move_counter
        self.row = row
        self.col = col

        self.board_size = len(self.board)

        if (self.board[self.row][self.col] == 'n'):
            for col in range(self.board_size):
                if (self.board[self.row][col] != 'n'):
                    self.col = col
                    break

    def color(self, row: int, col: int) -> str:
        return self.board[row][col]

    def can_move(self, row: int, col: int) -> bool:
        return row >= 0 and row < self.board_size and col >= 0 and col < self.board_size and self.color(row, col) != 'n'

    def swap(self, color1: str, color2: str) -> str:
        colors = {'r', 'y', 'b'}
        color3 = colors - {color1, color2}
        return color3.pop()
    
    def goal_test(self) -> bool:
        return self.board == self.goal_board
