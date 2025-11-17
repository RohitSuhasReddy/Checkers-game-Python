# file_manager.py
# handles saving, loading and checking if game is finished

from game_logic import get_valid_moves


def save_board(board, turn, filename="checkers_save.txt"):
    """Saves the current board and turn to a text file."""
    try:
        f = open(filename, "w")
        # write each row of board
        for r in board:
            f.write(" ".join(r) + "\n")
        # write whose turn
        f.write("TURN " + turn + "\n")
        f.close()
        print("Game saved successfully.")
    except Exception as e:
        print("Error while saving:", e)


def load_board(filename="checkers_save.txt"):
    """Loads the board and turn info from the save file."""
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        # last line has turn
        last = lines[-1].strip()
        parts = last.split()
        if len(parts) == 2 and parts[0] == "TURN":
            turn = parts[1]
        else:
            print("Invalid save format.")
            return None, None

        # other lines = board rows
        board = []
        for line in lines[:-1]:
            row = line.strip().split()
            board.append(row)

        print("Game loaded.")
        return board, turn

    except FileNotFoundError:
        print("Save file not found.")
        return None, None
    except Exception as e:
        print("Error while loading:", e)
        return None, None


def game_over(board, player):
    """Checks if given player has no pieces or moves left."""
    has_piece = False

    # check if player still has pieces
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "." and piece[0] == player:
                has_piece = True
                break

    if not has_piece:
        return True

    # check if any valid move exists
    moves = get_valid_moves(board, player)
    if not moves:
        return True

    return False
