import keyboard

class Amado:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.colors = {'r', 'y', 'b'}
        (self.row, self.col) = (0, 0)

    def swap(self, color1, color2):
        color3 = self.colors - {color1, color2}
        return color3.pop()

    def up(self):
        if self.row > 0:
            self.move(self.row - 1, self.col)

    def down(self):
        if self.row < self.size - 1:
            self.move(self.row + 1, self.col)

    def left(self):
        if self.col > 0:
            self.move(self.row, self.col - 1)

    def right(self):
        if self.col < self.size - 1:
            self.move(self.row, self.col + 1)

    def move(self, row, col):
        color1 = self.board[self.row][self.col]
        color2 = self.board[row][col]
        if color1 != color2:
            self.board[row][col] = self.swap(color1, color2)
        (self.row, self.col) = (row, col)

    def show(self):
        for row in range(self.size):
            print ("| ", end = "")
            for col in range(self.size):
                if (row, col) == (self.row, self.col):
                    print(self.board[row][col].upper(), end = "")
                else:
                    print(self.board[row][col], end = "")
                print(" | ", end = "")
            print()
        print()

if __name__ == "__main__":
    board = [
            ['y', 'y', 'y', 'b'],
            ['r', 'r', 'b', 'b'],
            ['r', 'b', 'b', 'b'],
            ['y', 'b', 'y', 'r'],
        ]

    game = Amado(board)

    while True:
        game.show()
        key = keyboard.read_key()
        if keyboard.is_pressed('w'):
            game.up()
        elif keyboard.is_pressed('a'):
            game.left()
        elif keyboard.is_pressed('s'):
            game.down()
        elif keyboard.is_pressed('d'):
            game.right()
        elif keyboard.is_pressed('q'):
            break
