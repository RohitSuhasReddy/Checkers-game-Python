EMPTY = " "   # empty square

class Board:
    def __init__(self):
        #  To build an 8x8 checker board
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.create_initial_board()

    
    def create_initial_board(self):
        """
        r = red man
        R = red king
        b = black man
        B = black king
          = empty
        """

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:      # playable dark squares
                    if row < 3:
                        self.board[row][col] = "b"    # black coin
                    elif row > 4:
                        self.board[row][col] = "r"    # red coin
                    else:
                        self.board[row][col] = EMPTY
                else:
                    self.board[row][col] = EMPTY

    def print_board(self):
        print("\n     1   2   3   4   5   6   7   8")
        print("    ---------------------------------")

        for row in range(8):
            print(f" {row+1} |", end=" ")
            for col in range(8):
                print(self.board[row][col], end=" | ")
            print("\n    ---------------------------------")


    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, value):
        self.board[row][col] = value


    def save_board(self, filename="savefile.txt"):
        with open(filename, "w") as f:
            for row in self.board:
                f.write(" ".join(row) + "\n")
        print(f"Board saved to {filename}")


    def load_board(self, filename="savefile.txt"):
        with open(filename, "r") as f:
            rows = f.read().strip().split("\n")

        for r in range(8):
            cols = rows[r].split()
            for c in range(8):
                self.board[r][c] = cols[c]

        print(f"Board loaded from {filename}")