from board import Board
from Game_logic import GameLogic
from File_manager import FileManager,load_game,save_game
from Menu import menu_display, menu_main, user_choice, clear_screen, Color, how_to_play, credits, print_thankyou


def user_move():
    try:
        r1, c1, r2, c2 = map(int, input("Your move: ").split())
        return (r1 - 1, c1 - 1), (r2 - 1, c2 - 1) 
    except:
        print(f"{Color.RED}INVALID INPUT! Please enter 4 numbers separated by spaces.{Color.RESET}")
        return user_move()


def start_new_game():
    board_obj = Board()
    logic = GameLogic(board_obj.board)
    current_player = "r"     # Red always starts

    print(f"{Color.CYAN}\n===================== NEW GAME STARTED ====================={Color.RESET}")
    board_obj.print_board()

    while True:
        print(f"{Color.BLUE}\nPlayer {current_player.upper()}'s turn{Color.RESET}")

        start, end =user_move()
        valid, message = logic.is_valid_move(start, end, current_player)

        if not valid:
            print(f"{Color.RED}Invalid move → {message}{Color.RESET}")
            continue

        # Apply move
        logic.move_piece(start, end)
        board_obj.print_board()

        # Check if opponent can move; if not → win
        opponent = "b" if current_player == "r" else "r"
        if not logic.has_any_valid_moves(opponent):
            print(f"{Color.GREEN} Player {current_player.upper()} WINS! {Color.RESET}")
            break

        # Switch player
        current_player = opponent

        # Offer save option
        ch = input(f"{Color.YELLOW}\nDo you want to save the game? (y/n): {Color.RESET}").lower()
        if ch == 'y':
            save_game(board_obj.board, current_player)
            print(f"{Color.GREEN}====================== Game Saved Successfully!! ======================{Color.RESET}")

def load_save_game():
    try:
        board_matrix, player = load_game()
    except:
        print(f"{Color.RED}\nNo saved game found or file is corrupted.{Color.RESET}")
        return

    board_obj = Board()
    board_obj.board = board_matrix

    logic = GameLogic(board_obj.board)
    current_player = player

    print(f"{Color.GREEN}\n========================== SAVED GAME LOADED =========================={Color.RESET}")
    board_obj.print_board()

    while True:
        print(f"{Color.BLUE}\nPlayer {current_player.upper()}'s turn{Color.RESET}")

        start, end =user_move()
        valid, message = logic.is_valid_move(start, end, current_player)

        if not valid:
            print(f"{Color.RED}Invalid move → {message}{Color.RESET}")
            continue

        logic.move_piece(start, end)
        board_obj.print_board()

        opponent = "b" if current_player == "r" else "r"
        if not logic.has_any_valid_moves(opponent):
            print(f"{Color.GREEN} Player {current_player.upper()} WINS! {Color.RESET}")
            break

        current_player = opponent

        ch = input(f"{Color.YELLOW}\nDo you want to save the game? (y/n): {Color.RESET}").lower()
        if ch == 'y':
            save_game(board_obj.board, current_player)
            print(f"{Color.GREEN}====================== Game Saved Successfully!! ======================{Color.RESET}")

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

        
