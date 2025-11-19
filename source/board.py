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
board = Board()
board.print_board() 

    