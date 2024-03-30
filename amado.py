class Amado:
    def __init__(self, board: list, row: int, col: int):
        self.board = board
        self.row = row
        self.col = col

        self.board_size = len(self.board)

        if self.board[self.row][self.col] == 'n':
            for col in range(self.board_size):
                if self.board[self.row][col] != 'n':
                    self.col = col
                    break

    def __hash__(self) -> int:
        return hash((tuple(map(tuple, self.board)), self.row, self.col))
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Amado):
            return False
        return self.col == other.col and self.row == other.row and self.board == other.board
        
    def current_color(self) -> str:
        return self.board[self.row][self.col]

    def color(self, row: int, col: int) -> str:
        return self.board[row][col]

    def can_move(self, row: int, col: int) -> bool:
        return row >= 0 and row < self.board_size and col >= 0 and col < self.board_size and self.color(row, col) != 'n'
