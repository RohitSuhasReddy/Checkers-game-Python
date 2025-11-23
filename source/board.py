EMPTY = "."   # empty square

class Board:
    def __init__(self):
        # -*-To build an 8x8 checker board.-*-
        # -*-Every position starts empty; pieces will be placed later.-*-
        self.board = [[EMPTY for _ in range(8)] for _ in range(8)]
        self.create_initial_board()

    # -*- Initial board set-up -*-
    def create_initial_board(self):
        """
        r = red man
        R = red king
        b = black man
        B = black king
        . = empty
        """

        for row in range(8):
            for col in range(8):
                # -*-check whether the square is playable or not.-*-
                if (row + col) % 2 == 1:      # -*-playable squares if (row+col = odd)-*-
                    if row < 3:
                        self.board[row][col] = "b"    # black man
                    elif row > 4:
                        self.board[row][col] = "r"    # red man
                    else:
                        self.board[row][col] = EMPTY

                # -*-These squares are always empty and not used to play.-*-
                else:
                    self.board[row][col] = EMPTY

    # -*-Numbering the rows and cols.-*-
    def print_board(self):
        print("\n     1   2   3   4   5   6   7   8")
         #-*- Good looking board with corne walls.-*-
        print("    ---------------------------------")

        for row in range(8):
            print(f" {row+1} |", end=" ")
            for col in range(8):
                #-*- Printing each square with a border for better readability.-*-
                print(self.board[row][col], end=" | ")
            print("\n    ---------------------------------")

    # -*-Returning whatever piece (or empty space) exists at this position just before.-*-
    def get_piece(self, row, col):
        return self.board[row][col]

    # -*- Replacing the piece at a specific board location with new value.-*-
    def set_piece(self, row, col, value):
        self.board[row][col] = value

    # -*- Saving the current board version to a text file.This is useful to pasue and resume the game at any time we want.-*-
    def save_board(self, filename="savefile.txt"):
        with open(filename, "w") as f:
            for row in self.board:
                # -*- This joins all columns with spaces to make the file  readable. -*-
                f.write(" ".join(row) + "\n")
        print(f"Board saved to {filename}")

    # -*- Load a previously saved board from a file.This allows us to resume the game exactlty where we left the game. -*-
    def load_board(self, filename="savefile.txt"):
        with open(filename, "r") as f:
            rows = f.read().strip().split("\n")

        for r in range(8):
            cols = rows[r].split()
            for c in range(8):
                # -*- Restoring each square one by one. -*-
                self.board[r][c] = cols[c]

        print(f"Board loaded from {filename}")