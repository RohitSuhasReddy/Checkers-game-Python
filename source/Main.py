from board import Board
from Game_logic import GameLogic
from File_manager import FileManager
from Menu import menu_display, menu_main, user_choice, clear_screen, Color, how_to_play, credits, print_thankyou


def user_move():
    while(2>1):
        raw = input("Your move (r1 c1 r2 c2) or 's' to save or 'l' to load: ").strip()
        if (raw.lower() == 's'):
            return 'save'
        if (raw.lower() == 'l'):
            return 'load'
        parts = raw.split()
        if (len(parts) != 4 or not all(p.isdigit() for p in parts)):
            print(f"{Color.RED}INVALID INPUT! Enter 4 numbers like: 6 1 5 2{Color.RESET}")
            continue
        r1, c1, r2, c2 = map(int, parts)
        return (r1 - 1, c1 - 1), (r2 - 1, c2 - 1)



def start_new_game():
    board_obj = Board()
    logic = GameLogic(board_obj.board)
    current_player = 'r'   # red starts
    clear_screen()

    # File manager instance (attach board and player)
    fm = FileManager(board_obj, current_player)

    print(f"{Color.CYAN}\n==================== NEW GAME STARTED ===================={Color.RESET}")
    board_obj.print_board()

    while True:
        print(f"\n{Color.BLUE}Player {current_player.upper()}'s turn{Color.RESET}")

        mv = user_move()

        # Save request
        if mv == 'save':
            fm.board_obj = board_obj
            fm.current_player = current_player
            fm.save_game()
            input("Press ENTER to continue...")
            continue

        # Load request
        if mv == 'load':
            loaded_board, loaded_turn = fm.load_game()
            if loaded_board:
                board_obj.board = loaded_board
                current_player = loaded_turn
                logic = GameLogic(board_obj.board)  # re-create logic with loaded board
                print("Loaded board. Continuing...")
                board_obj.print_board()
            else:
                print("No saved game found.")
            input("Press ENTER to continue...")
            continue

        # Normal move
        start, end = mv
        sr, sc = start
        er, ec = end

        # Validate using wrapper is_valid_move (we added to GameLogic)
        valid, message = logic.is_valid_move(start, end, current_player)
        if not valid:
            print(f"{Color.RED}Invalid move: {message}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        # Apply move by calling process_move (expects 4 ints)
        ok, msg, new_player = logic.process_move(sr, sc, er, ec)
        if not ok:
            print(f"{Color.RED}{msg}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        # Successful move
        print(f"{Color.GREEN}{msg}{Color.RESET}")
        board_obj.print_board()

        # Save automatically after a successful move if you want:
        fm.board_obj = board_obj
        fm.current_player = new_player
        fm.save_game()

        # Update current player and logic
        current_player = new_player
        logic.current_player = current_player

        # Check game over: if opponent has no moves
        opponent = 'b' if current_player == 'r' else 'r'
        if not logic.has_any_valid_moves(opponent):
            print(f"\n{Color.GREEN}GAME OVER! Player {current_player.upper()} wins!{Color.RESET}")
            input("Press ENTER to return to menu...")
            break

def load_saved_game():
    clear_screen()
    print(f"{Color.CYAN}\n===================== SAVED GAME LOADED ====================={Color.RESET}")

    board_obj = Board()
    fm = FileManager(board_obj)
    loaded_board, current_player = fm.load_game()

    board_obj.board = loaded_board

    board_obj.print_board()
    print(f"\n{Color.BLUE}Player {current_player.upper()}'s turn{Color.RESET}")

    return board_obj, current_player


def load_save_game():
    # create a board and FileManager, then call load
    board_obj = Board()
    fm = FileManager(board_obj, 'r')
    loaded_board, loaded_turn = fm.load_game()
    if not loaded_board:
        print("No saved game to load.")
        input("Press ENTER to return...")
        return
    board_obj.board = loaded_board
    current_player = loaded_turn
    logic = GameLogic(board_obj.board)
    clear_screen()
    print(f"{Color.CYAN}\n==================== SAVED GAME LOADED ===================={Color.RESET}")
    board_obj.print_board()

    # then run the same loop as start_new_game but using loaded board
    while True:
        print(f"\n{Color.BLUE}Player {current_player.upper()}'s turn{Color.RESET}")
        mv = user_move()
        if mv == 'save':
            fm.board_obj = board_obj
            fm.current_player = current_player
            fm.save_game()
            input("Press ENTER to continue...")
            continue
        if mv == 'load':
            print("Already loaded.")
            input("Press ENTER to continue...")
            continue

        start, end = mv
        sr, sc = start
        er, ec = end

        valid, message = logic.is_valid_move(start, end, current_player)
        if not valid:
            print(f"{Color.RED}Invalid move: {message}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        ok, msg, new_player = logic.process_move(sr, sc, er, ec)
        if not ok:
            print(f"{Color.RED}{msg}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        print(f"{Color.GREEN}{msg}{Color.RESET}")
        board_obj.print_board()

        fm.board_obj = board_obj
        fm.current_player = new_player
        fm.save_game()

        current_player = new_player
        logic.current_player = current_player

        opponent = 'b' if current_player == 'r' else 'r'
        if not logic.has_any_valid_moves(opponent):
            print(f"\n{Color.GREEN}GAME OVER! Player {current_player.upper()} wins!{Color.RESET}")
            input("Press ENTER to return to menu...")
            break

#Main Module Definition

def main_module():
    while(2>1):
        choice=menu_main()
        if(choice==1):
            start_new_game()
        elif(choice==2):
            load_save_game()
        elif(choice==3):
            how_to_play()
        elif(choice==4):
            credits()
        elif(choice==5):
            print_thankyou()
            break

if __name__ == "__main__":      
    main_module()

        
