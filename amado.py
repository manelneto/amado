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

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.board == other.board and self.row == other.row and self.col == other.col
        else:
            return False

    def __str__(self):
        res = '|'
        for row in range(self.board_size):
            for col in range(self.board_size):
                if row == self.row and col == self.col:
                    res += self.board[row][col].upper()
                else:
                    res += self.board[row][col]
            res += '|'
        return ' '.join(list(res))

    def color(self, row: int, col: int) -> str:
        return self.board[row][col]

    def can_move(self, row: int, col: int) -> bool:
        return row >= 0 and row < self.board_size and col >= 0 and col < self.board_size and self.color(row, col) != 'n'

    def swap(self, color1: str, color2: str) -> str:
        colors = {'r', 'y', 'b'}
        color3 = colors - {color1, color2}
        return color3.pop()
