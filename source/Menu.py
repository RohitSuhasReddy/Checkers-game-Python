import os

class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def credits():
    clear_screen()
    print(f"{Color.GREEN}==============================================CREDITS============================================================{Color.RESET}")
    print(f"""{Color.BLUE}
    Checkers(CLI Edition)
          Developed by:
          -P1: K.Nitheesh Board
          -P2: B.Rahul Logic
          -P3: Mayank File Manager
          -P4: S.Rohit Integration and Menu System
{Color.RESET}""")
    print("\n")
    print(f"{Color.GREEN}==================================================================================================================={Color.RESET}")
    input(f"{Color.GREEN}Press ENTER to return to MENU{Color.RESET}")

def how_to_play():
    clear_screen()
    print(f"{Color.GREEN}==============================================HOW to PLAY============================================================{Color.RESET}")

    print(f"{Color.CYAN}1. Pieces & Colors{Color.RESET}")
    print("""
- You will play as either RED or BLACK.
- Normal pieces can only move forward diagonally.
- When a piece reaches the last row on the opponents side, 
  it becomes a KING and can move in both directions.
""")

    print(f"{Color.CYAN}2. How Movement Works{Color.RESET}")
    print("""
- Moves are diagonal only.
- A normal move is one step into an empty diagonal square.
- Example of a simple move:
  
     r1 c1 r2 c2
     2 3 3 4   → This moves the piece from (2,3) to (3,4)
""")

    print(f"{Color.CYAN}3. Capturing Rules{Color.RESET}")
    print("""
- If an opponents piece is diagonally adjacent and the square behind it is empty,
  you MUST jump and capture it.
  
- Captures are mandatory in this game.

- Multi-jump is allowed:
  If after capturing one piece you can capture another,
  the game will force you to continue jumping.
""")

    print(f"{Color.CYAN}4. Ending the Game{Color.RESET}")
    print("""
The game ends when:
- One player has no pieces left, OR
- One player has no legal moves available.

The player with remaining movable pieces wins.
""")

    print(f"{Color.GREEN}==================================================================================================================={Color.RESET}")
    input(f"{Color.GREEN}Press ENTER to return to MENU{Color.RESET}")




def print_footer():
    footer=r"""
              /$$$$$$  /$$                           /$$                                    
             /$$__  $$| $$                          | $$                                    
            | $$  \__/| $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$   /$$$$$$   /$$$$$$$
            | $$      | $$__  $$ /$$__  $$ /$$_____/| $$  /$$/ /$$__  $$ /$$__  $$ /$$_____/
            | $$      | $$  \ $$| $$$$$$$$| $$      | $$$$$$/ | $$$$$$$$| $$  \__/|  $$$$$$ 
            | $$    $$| $$  | $$| $$_____/| $$      | $$_  $$ | $$_____/| $$       \____  $$
            |  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$$| $$       /$$$$$$$/
             \______/ |__/  |__/ \_______/ \_______/|__/  \__/ \_______/|__/      |_______/                                                
"""
    print(footer)

def print_thankyou():
    thankyou=r"""
            ___________.__                   __                       ._._.
            \__    ___/|  |__ _____    ____ |  | _____.__. ____  __ __| | |
              |    |   |  |  \\__  \  /    \|  |/ <   |  |/  _ \|  |  \ | |
              |    |   |   Y  \/ __ \|   |  \    < \___  (  <_> )  |  /\|\|
              |____|   |___|  (____  /___|  /__|_ \/ ____|\____/|____/ ____
                        \/     \/     \/     \/\/                  \/\/
"""
    print(thankyou)

def menu_display():
    clear_screen()
    print(f"{Color.GREEN}-------------------------------------------------------------------------------------------------------------------{Color.RESET}")
    print(f"{Color.GREEN}-------------------------------------------------------------------------------------------------------------------{Color.RESET}")
    print_footer()
    print("\n")
    print(f"{Color.GREEN}==============================================GAME MENU============================================================{Color.RESET}")
    print(f"{Color.BLUE}1.New Game{Color.RESET}")
    print(f"{Color.BLUE}2.Load Saved Game{Color.RESET}")
    print(f"{Color.BLUE}3.How to Play{Color.RESET}")
    print(f"{Color.BLUE}4.Credits{Color.RESET}")
    print(f"{Color.BLUE}5.Exit{Color.RESET}")
    print(f"{Color.GREEN}==================================================================================================================={Color.RESET}")


def user_choice():
    while(2>1):
        Response=int(input("Enter your Choice...."))
        if(Response>5 or Response <1):
            print(f"{Color.RED}INVALID MOVE! Enter a number between 1-5{Color.RESET}")
        else:
            return Response

def menu_main():
    while(2>1):
        menu_display()
        choice=user_choice()
        if(choice==1):
            return 1
        elif(choice==2):
            return 2
        elif(choice==3):
            how_to_play()
        elif(choice==4):
            credits()
        elif(choice==5):
            clear_screen()
            print(f"{Color.GREEN}==================================================================================================================={Color.RESET}")
            print_thankyou()
            print(f"{Color.GREEN}==================================================================================================================={Color.RESET}")
            exit()





