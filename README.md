# Checkers in CLI
                                                                                                        
## **Description:**
This project is a fully functional **Standard Checkers Game** which fully runs on CLI built using Python

### The Game Features:
-An 8X8 ASCII rendered board
-Complete Move Validating System
-Mandatory Capture System
-King Promotion
-Save and Load function
-A Clean and Colored UI

The Project is modular with seperate  -Board Handling
                                      -Game Logic
                                      -File Managment
                                      -Menu UI
                                      -Main Integration

# **Files Structure:**

   ## Source(Folder):
         board.py-->Board rendering.
         Game_logic.py-->Movement, captures, rules(Logic Engine).
         File_manager.py-->Saving and loading.
         Menu.py-->UI, color codes.
         Main.py-->Integration, Game loop.

# **Rules:**
1. **Pieces & Colors:**
- You will play as either RED or BLACK.
- Normal pieces can only move forward diagonally.
- When a piece reaches the last row on the opponents side, 
  it becomes a KING and can move in both directions.

2. **How Movement Works:**
- Moves are diagonal only.
- A normal move is one step into an empty diagonal square.
- Example of a simple move:
  
     r1 c1 r2 c2
     2 3 3 4   → This moves the piece from (2,3) to (3,4)

3. **Capturing Rules:**
- If an opponents piece is diagonally adjacent and the square behind it is empty,
  you MUST jump and capture it.
  
- Captures are mandatory in this game.

- Multi-jump is allowed:
  If after capturing one piece you can capture another,
  the game will force you to continue jumping.

4. **Ending the Game:**
 The game ends when:
- One player has no pieces left, OR
- One player has no legal moves available.

The player with remaining movable pieces wins.

# **Instructions/Notes:**
    1.Download the project using GIT link.
    2.Open the Source folder(Always run the game from inside this folder only).
    3. **VERY IMPORTANT!! Do not Rename the files.**
    4.Run the game from main.py 

# **Credits:**
## **Developed by:**
            -(P1) K.Nitheesh: Board
            -(P2) B.Rahul:  Game Logic
            -(P3) Mayank: File Manager
            -(P4) S.Rohit: Integration and Menu System and Documentation





