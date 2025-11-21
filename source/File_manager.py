# file_manager.py

EMPTY = "."

class FileManager:
    def _init_(self, board_obj, current_player):
        self.board_obj = board_obj      # Board object
        self.current_player = current_player  # "r" or "b"

    # ------------------------------------------------------
    # SAVE GAME
    # ------------------------------------------------------
    def save_game(self, filename="checkers_save.txt"):
        try:
            with open(filename, "w") as f:
                # save board
                for r in range(8):
                    f.write(" ".join(self.board_obj.board[r]) + "\n")

                # save current turn
                f.write("TURN " + self.current_player + "\n")

            print("Game saved successfully!")

        except Exception as e:
            print("Error saving game:", e)

    # ------------------------------------------------------
    # LOAD GAME
    # ------------------------------------------------------
    def load_game(self, filename="checkers_save.txt"):
        try:
            with open(filename, "r") as f:
                lines = f.read().strip().split("\n")

            # load board
            new_board = []
            for r in range(8):
                row = lines[r].split()
                new_board.append(row)

            # load turn
            info = lines[8].split()
            if info[0] == "TURN":
                self.current_player = info[1]
            else:
                print("Corrupted save file!")
                return None, None

            # update board object
            self.board_obj.board = new_board

            print("Game loaded successfully!")
            return self.board_obj, self.current_player

        except Exception as e:
            print("Error loading game:", e)
            return None, None