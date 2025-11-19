class Piece:
    def __init__(self, color, row, col):

        self.color = color      # "RED" or "BLACK"
        self.row = row
        self.col = col
        self.king = False       # Level of piece.
class Board:
    def __init__(self):

        # Build an 8x8 board filled with None
        self.board = [[None for _ in range(1,9)] for _ in range(1,9)]
        self.create_initial_board()

    # 1) Convert a Piece object → ASCII Character
    
    def piece_to_char(self, piece):
        if piece is None:
            return " "       # empty square
        
        if piece.color == "RED":
            return "R" if piece.king else "r"
        
        if piece.color == "BLACK":
            return "B" if piece.king else "b"

    # 2) Print the board in ASCII
    
    def print_board(self):
        print("\n        1     2     3     4     5     6     7     8")
        print("     ---------------------------------------------------")

        for row in range(8):
            print(f" {row+1}  |", end="")

            for col in range(8):
                p = self.board[row][col]
                char = self.piece_to_char(p)
                
                # Each square is 5 characters wide
                print(f"  {char}  |", end="")

            print("\n     ---------------------------------------------------")
    

    # 3) Initial Setup for Checkers
    def create_initial_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  

                    if row < 3:           # black top rows
                        self.board[row][col] = Piece("BLACK", row, col)

                    elif row > 4:         # red bottom rows
                        self.board[row][col] = Piece("RED", row, col)



    def board_to_text(self):
        lines = []
        for row in range(8):
            line = []
            for col in range(8):
                p = self.board[row][col]

                if p is None:
                    line.append("_")        # Empty
                elif p.color == "RED":
                    line.append("R" if p.king else "r")
                elif p.color == "BLACK":
                    line.append("B" if p.king else "b")

            lines.append(" ".join(line))
        return "\n".join(lines)


    def save_board(self, filename="savefile.txt"):
        text = self.board_to_text()
        with open(filename, "w") as f:
            f.write(text)
        print(f"Board saved to {filename}")


    def load_board(self, filename="savefile.txt"):
        with open(filename, "r") as f:
            rows = f.read().strip().split("\n")

        for r in range(8):
            cols = rows[r].split(" ")
            for c in range(8):
                char = cols[c]

                if char == "_":
                    self.board[r][c] = None

                elif char == "r":
                    self.board[r][c] = Piece("RED", r, c)

                elif char == "R":
                    p = Piece("RED", r, c)
                    p.king = True
                    self.board[r][c] = p

                elif char == "b":
                    self.board[r][c] = Piece("BLACK", r, c)

                elif char == "B":
                    p = Piece("BLACK", r, c)
                    p.king = True
                    self.board[r][c] = p

        print(f"Board loaded from {filename}")




board = Board()
board.print_board() 

    