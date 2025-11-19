# file_manager.py
# This class is used to save the game, load the game, and check if the game is over.

from board import Piece
from game_logic import gamelogicin


class FileManager:
    # Constructor stores board object and current player's turn
    def __init__(self, board_obj, current_player):
        self.board_obj = board_obj          # Board() object
        self.current_player = current_player   # "r" or "b"

    
    # SAVE GAME FUNCTION
    
    def save_game(self, filename="checkers_save.txt"):
        """
        This function writes the whole board into a text file.
        Each piece is saved as: r, R, b, B or .
        """
        try:
            # open the file in write mode
            f = open(filename, "w")

            # write the 8 rows of the board one by one
            for r in range(8):
                row_items = []     # temporary list to hold characters

                for c in range(8):
                    piece = self.board_obj.board[r][c]

                    # empty place
                    if piece is None:
                        row_items.append(".")

                    # not empty → convert Piece object into a character
                    else:
                        if piece.color == "RED":
                            if piece.king:
                                row_items.append("R")   # red king
                            else:
                                row_items.append("r")   # red normal
                        else:
                            if piece.king:
                                row_items.append("B")   # black king
                            else:
                                row_items.append("b")   # black normal

                # join characters with space and write to file
                f.write(" ".join(row_items) + "\n")

            # save whose turn it is at the end
            f.write("TURN " + self.current_player + "\n")

            f.close()
            print("Game saved.")

        except:
            print("Could not save the game.")

    
    # LOAD GAME FUNCTION
    
    def load_game(self, filename="checkers_save.txt"):
        """
        Reads the saved text file and rebuilds the board using Piece objects.
        """
        try:
            # open file in read mode
            f = open(filename, "r")
            lines = f.readlines()
            f.close()

            # create a fresh empty board (8x8)
            new_board = [[None for _ in range(8)] for _ in range(8)]

            # read the first 8 lines for pieces
            for r in range(8):
                parts = lines[r].strip().split()

                for c in range(8):
                    ch = parts[c]   # character such as r, R, b, B, .

                    # empty square
                    if ch == ".":
                        new_board[r][c] = None

                    # create RED piece
                    elif ch == "r":
                        p = Piece("RED", r, c)
                        new_board[r][c] = p

                    elif ch == "R":
                        p = Piece("RED", r, c)
                        p.king = True        # set king = True
                        new_board[r][c] = p

                    # create BLACK piece
                    elif ch == "b":
                        p = Piece("BLACK", r, c)
                        new_board[r][c] = p

                    elif ch == "B":
                        p = Piece("BLACK", r, c)
                        p.king = True
                        new_board[r][c] = p

            # last line should contain TURN r or TURN b
            last = lines[8].strip().split()
            if last[0] == "TURN":
                self.current_player = last[1]
            else:
                print("Save file is corrupted.")
                return None, None

            # replace the board with the loaded one
            self.board_obj.board = new_board

            print("Game loaded.")
            return self.board_obj, self.current_player

        except:
            print("Could not load the game.")
            return None, None

    
    # GAME OVER CHECK FUNCTION
    
    def game_over(self):
        """
        Game ends if:
        1) current player has no pieces left
        2) current player has no moves left
        """

        
        # Check if player still has any pieces
    
        has_piece = False

        for r in range(8):
            for c in range(8):
                piece = self.board_obj.board[r][c]
                if piece is not None:
                    # if player is red, search for RED pieces
                    if self.current_player == "r" and piece.color == "RED":
                        has_piece = True
                    # if player is black, search for BLACK pieces
                    if self.current_player == "b" and piece.color == "BLACK":
                        has_piece = True

        # no pieces → game over
        if not has_piece:
            return True

        
        # Convert Board to simple r/R/b/B/. board
        # because gamelogicin works with chars
        
        simple_board = []
        for r in range(8):
            row2 = []
            for c in range(8):
                piece = self.board_obj.board[r][c]

                if piece is None:
                    row2.append(".")
                else:
                    if piece.color == "RED":
                        if piece.king:
                            row2.append("R")
                        else:
                            row2.append("r")
                    else:
                        if piece.king:
                            row2.append("B")
                        else:
                            row2.append("b")

            simple_board.append(row2)

        # create logic object to check possible moves
        logic = gamelogicin(simple_board, self.current_player)

        
        # Check captures first
        
        captures = logic.get_all_captures()
        if len(captures) > 0:
            return False   # there is at least one capture move

        
        # Check normal moves (no capture available)
        
        for r in range(8):
            for c in range(8):
                if logic.is_own_piece(r, c):
                    piece_letter = simple_board[r][c]

                    # get normal movement directions
                    dirs = logic.get_allowed_directions(piece_letter)
                    for dr, dc in dirs:
                        nr = r + dr
                        nc = c + dc

                        # inside board and empty square?
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            if simple_board[nr][nc] == ".":
                                return False   # normal move exists

        # if no captures and no normal moves → game over
        return True
