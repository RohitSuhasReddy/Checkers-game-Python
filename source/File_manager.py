class FileManager:
    def __init__(self, board_obj=None, current_player='r'):
        self.board_obj = board_obj
        self.current_player = current_player

    def save_game(self, filename="checkers_save.txt"):
        try:
            with open(filename, "w") as f:
                for r in range(8):
                    f.write(" ".join(self.board_obj.board[r]) + "\n")
                f.write("TURN " + self.current_player + "\n")
            print("Game saved successfully!")
        except Exception as e:
            print("Error saving game:", e)

    def load_game(self, filename="checkers_save.txt"):
        try:
            with open(filename, "r") as f:
                lines = f.read().strip().split("\n")
            new_board = []
            for r in range(8):
                row = lines[r].split()
                new_board.append(row)
            turn_line = lines[8].split()
            new_turn = turn_line[1]
            print("Game loaded successfully!")
            return new_board, new_turn
        except Exception as e:
            print("Error loading game:", e)
            return None, None
