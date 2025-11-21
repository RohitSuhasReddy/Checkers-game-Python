EMPTY = "."   # empty square

class Board:
    def __init__(self):
        # Build an 8x8 checkers board
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.create_initial_board()

    # ------------------------------------------------------------
    # INITIAL SETUP
    # ------------------------------------------------------------

    def create_initial_board(self):
        """
        r = red piece
        R = red king
        b = black piece
        B = black king
        . = empty
        """

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:      # playable dark squares
                    if row < 3:
                        self.board[row][col] = "b"    # black piece
                    elif row > 4:
                        self.board[row][col] = "r"    # red piece
                    else:
                        self.board[row][col] = EMPTY
                else:
                    self.board[row][col] = EMPTY

    # ------------------------------------------------------------
    # ASCII BOARD PRINTER
    # ------------------------------------------------------------
    def print_board(self):
        print("\n      1   2   3   4   5   6   7   8")
        print("    ----------------------------------------")

        for row in range(8):
            print(f" {row+1} |", end=" ")
            for col in range(8):
                print(self.board[row][col], end=" | ")
            print("\n    ---------------------------------")

    # ------------------------------------------------------------
    # GET / SET PIECES (used by P2 logic)
    # ------------------------------------------------------------
    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, value):
        self.board[row][col] = value

    # ------------------------------------------------------------
    # SAVE GAME (character based, compatible with P2)
    # ------------------------------------------------------------
    def save_board(self, filename="savefile.txt"):
        with open(filename, "w") as f:
            for row in self.board:
                f.write(" ".join(row) + "\n")
        print(f"Board saved to {filename}")

    # ------------------------------------------------------------
    # LOAD GAME
    # ------------------------------------------------------------
    def load_board(self, filename="savefile.txt"):
        with open(filename, "r") as f:
            rows = f.read().strip().split("\n")

        for r in range(8):
            cols = rows[r].split()
            for c in range(8):
                self.board[r][c] = cols[c]

        print(f"Board loaded from {filename}")