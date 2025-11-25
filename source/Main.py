from board import Board
from Game_logic import GameLogic
from File_manager import FileManager
from Menu import menu_main, clear_screen, Color, how_to_play, credits, print_thankyou

#1.Takes the input
#2.If it is S or s then returns save
#3.If it is L or l then return load
#4.Checks the coordinates input


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

#1.Clears the screen
#2.Creates a new fresh board
#3.Sets the player turn to r
#4.Sets the game logic

def start_new_game():
    board_obj = Board()
    current_player = 'r'
    logic = GameLogic(board_obj.board, current_player)

    clear_screen()

    #Enables saving
    fm = FileManager(board_obj, current_player)

    print(f"{Color.CYAN}\n==================== NEW GAME STARTED ===================={Color.RESET}")
    board_obj.print_board()

    while(2>1):
        print(f"\n{Color.BLUE}Player {current_player.upper()}'s turn{Color.RESET}")

        mv = user_move()

        #Save request
        if(mv == 'save'):
            fm.board_obj = board_obj
            fm.current_player = current_player
            fm.save_game()
            input("Press ENTER to continue...")
            continue

        #Load request
        if(mv == 'load'):
            loaded_board, loaded_turn = fm.load_game()
            if loaded_board:
                board_obj.board = loaded_board
                current_player = loaded_turn
                logic = GameLogic(board_obj.board, current_player)
                print("Loaded board. Continuing...")
                board_obj.print_board()
            else:
                print("No saved game found.")
            input("Press ENTER to continue...")
            continue

        #Normal move
        start, end = mv
        sr, sc = start
        er, ec = end

        #Validate using is_valid_move
                #Ensures that the squares are well within the boundaries.
                #Checks if the player is moving their own piece or not.
                #Checks mandatory capture rule.
                #Checks for capture is feasible or not, if not then normal move.
        valid, message = logic.is_valid_move(start, end, current_player)
        if not valid:
            print(f"{Color.RED}Invalid move: {message}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        #Apply move by calling process_move
                #Validates the move,
                #Applies it.
                #Switches the turn.
        ok, msg, new_player = logic.process_move(sr, sc, er, ec)
        if not ok:
            print(f"{Color.RED}{msg}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        #Successful move
        print(f"{Color.GREEN}{msg}{Color.RESET}")
        board_obj.print_board()

        #Auto Save after a successful move
        fm.board_obj = board_obj
        fm.current_player = new_player
        fm.save_game()

        #Update current player and logic
        current_player = new_player
        logic.current_player = current_player

        #Checking Game Over
        opponent = 'b' if current_player == 'r' else 'r'
        if not logic.has_any_valid_moves(opponent):
            print(f"\n{Color.RED}GAME OVER!!! Player {current_player.upper()} Wins!!{Color.RESET}")
            input("Press ENTER to return to menu...")
            break

#1.Clears the screen
#2.Loads the board saved earlier
#3.Loads the current player turn
#4.Starts the Game from the exact position leftover
#5.Mostly same as start_new_game()


def load_save_game():
    board_obj = Board()
    fm = FileManager(board_obj, 'r')
    loaded_board, loaded_turn = fm.load_game()
    if not loaded_board:
        print("No saved game to load.")
        input("Press ENTER to return...")
        return
    board_obj.board = loaded_board
    current_player = loaded_turn
    logic = GameLogic(board_obj.board, current_player)
    clear_screen()
    print(f"{Color.CYAN}\n==================== SAVED GAME LOADED ===================={Color.RESET}")
    board_obj.print_board()

    #Same as the start_new_game() mostly
    while(2>1):
        print(f"\n{Color.BLUE}Player {current_player.upper()}'s turn{Color.RESET}")

        mv = user_move()

        #Save Request
        if mv == 'save':
            fm.board_obj = board_obj
            fm.current_player = current_player
            fm.save_game()
            input("Press ENTER to continue...")
            continue

        #Load Request
        if mv == 'load':
            print("Already loaded.")
            input("Press ENTER to continue...")
            continue

        #Normal Move
        start, end = mv
        sr, sc = start
        er, ec = end

        #Validate using is_valid_move()
        valid, message = logic.is_valid_move(start, end, current_player)
        if not valid:
            print(f"{Color.RED}Invalid move: {message}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        #Apply move by calling process_move
        ok, msg, new_player = logic.process_move(sr, sc, er, ec)
        if not ok:
            print(f"{Color.RED}{msg}{Color.RESET}")
            input("Press ENTER to continue...")
            continue

        #Successful move
        print(f"{Color.GREEN}{msg}{Color.RESET}")
        board_obj.print_board()

        #Auto Save after a successful move
        fm.board_obj = board_obj
        fm.current_player = new_player
        fm.save_game()

        #Update current player and logic
        current_player = new_player
        logic.current_player = current_player

        #Checking Game Over
        opponent = 'b' if current_player == 'r' else 'r'
        if not logic.has_any_valid_moves(opponent):
            print(f"\n{Color.GREEN}GAME OVER!!! Player {current_player.upper()} Wins!!{Color.RESET}")
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

        
