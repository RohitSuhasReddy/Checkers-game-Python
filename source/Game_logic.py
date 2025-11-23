EMPTY = "."
class GameLogic:
    def __init__(self, board, current_player='r'):
        # Store the 8x8 board and track whose turn it is ('r' or 'b')
        self.board = board
        self.current_player = current_player
    def is_inside(self, r, c):
        # Check whether (r,c) is inside the 8×8 board
        return 0 <= r < 8 and 0 <= c < 8 
    def is_own_piece(self, r, c, player=None):
        # Returns True if the square contains a piece that belongs to 'player'
        if player is None:
            player = self.current_player
        # Outside board
        if not self.is_inside(r, c):
            return False
        piece = self.board[r][c]
        # Empty square means not player's piece
        if piece == EMPTY:
            return False
        # Compare lowercase so 'r' matches 'R' (kings)
        return piece.lower() == player.lower()
    def _is_opponent_player(self, r, c, player):
        # Check if the piece at (r,c) belongs to the opponent of 'player'
        if not self.is_inside(r, c):
            return False
        piece = self.board[r][c]
        if piece == EMPTY:
            return False
        # If lowercase values differ → opponent
        return piece.lower() != player.lower()
    def is_valid_move(self, start, end, player=None):
        # Determines whether ANY move (normal or capture) is valid
        sr, sc = start
        er, ec = end
        if player is None:
            player = self.current_player
        # 1. Both squares must be inside board
        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False, "out_of_bounds"
        # 2. Player must move their own piece
        if not self.is_own_piece(sr, sc, player):
            return False, "not_your_piece"
        # 3. Check mandatory capture rule
        captures = self.get_all_captures()
        if (sr, sc) in captures:  
            # If this piece can capture, check if end square is a valid capture move
            if (er, ec) in captures[(sr, sc)]:
                return True, "valid_capture"
            return False, "must_capture"
        # 4. If no capture available, check normal move
        if self.is_valid_normal_move(sr, sc, er, ec):
            return True, "valid_normal"
        return False, "invalid_move"
    def get_allowed_directions(self, piece):
        # For simple moves (distance 1), define allowed directions
        if piece in ("R", "B"):  # Kings can move any diagonal
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece == "r":  # red moves upward
            return [(-1, -1), (-1, 1)]
        if piece == "b":  # black moves downward
            return [(1, -1), (1, 1)]
        return []
    def get_all_directions(self):
        # Return all diagonal direction offsets used for capture checks
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    def is_valid_normal_move(self, sr, sc, er, ec):
        # Validates a simple diagonal step (no capturing
        # 1. Both squares must be inside
        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False
        piece = self.board[sr][sc]
        if piece == EMPTY:
            return False
        # 2. End square MUST be empty
        if self.board[er][ec] != EMPTY:
            return False
        dr = er - sr
        dc = ec - sc
        # 3. Must move exactly 1 diagonal step
        if abs(dr) != 1 or abs(dc) != 1:
            return False
        # 4. Normal pieces cannot move backward
        if piece in ("r", "b"):
            forward = -1 if piece == "r" else 1  
            if dr != forward:
                return False
        return True
    def is_valid_capture_move(self, sr, sc, er, ec):
        # Validates a capturing jump
        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False
        piece = self.board[sr][sc]
        if piece == EMPTY:
            return False
        if self.board[er][ec] != EMPTY:
            return False
        # Capture requires jumping exactly 2 tiles diagonally
        dr = er - sr
        dc = ec - sc
        if abs(dr) != 2 or abs(dc) != 2:
            return False
        # Middle tile (the piece being jumped)
        mid_r = sr + dr // 2
        mid_c = sc + dc // 2
        if not self.is_inside(mid_r, mid_c):
            return False
        # Middle tile must contain enemy
        if not self._is_opponent_player(mid_r, mid_c, piece):
            return False
        # Normal pieces must capture forward only
        if piece in ("r", "b"):
            forward = -1 if piece == "r" else 1
            if dr != 2 * forward:
                return False
        return True
    def _has_capture_from(self, r, c):
        # Check if this piece can capture in ANY direction
        piece = self.board[r][c]
        if piece == EMPTY:
            return False
        for dr, dc in self.get_all_directions():
            er = r + 2 * dr
            ec = c + 2 * dc
            if self.is_valid_capture_move(r, c, er, ec):
                return True
        return False
    def get_all_captures(self):
        # Return dictionary of all pieces that can capture and their possible end positions
        captures = {}
        for r in range(8):
            for c in range(8):
                if self.is_own_piece(r, c):
                    piece_moves = []
                    # Try all 4 possible capture directions
                    for dr, dc in self.get_all_directions():
                        er = r + 2 * dr
                        ec = c + 2 * dc
                        if self.is_valid_capture_move(r, c, er, ec):
                            piece_moves.append((er, ec))
                    if piece_moves:
                        captures[(r, c)] = piece_moves
        return captures
    def apply_normal_move(self, sr, sc, er, ec):
        # Execute a simple step move on the board
        piece = self.board[sr][sc]
        self.board[sr][sc] = EMPTY
        self.board[er][ec] = piece
        self.promote_to_king(er, ec)
    def apply_capture_move(self, sr, sc, er, ec):
        # Execute capture: remove opponent piece and move your piec
        piece = self.board[sr][sc]
        mid_r = (sr + er) // 2
        mid_c = (sc + ec) // 2
        # Remove captured piece
        self.board[mid_r][mid_c] = EMPTY
        # Move piece
        self.board[sr][sc] = EMPTY
        self.board[er][ec] = piece
    def has_more_captures(self, r, c):
        # After a capture, check if the same piece can capture again
        return self._has_capture_from(r, c)
    def promote_to_king(self, r, c):
        # Promote a piece to king when reaching the last row
        piece = self.board[r][c]
        if piece == "r" and r == 0:
            self.board[r][c] = "R"
        elif piece == "b" and r == 7:
            self.board[r][c] = "B"
    def switch_player(self):
        # Change turn from 'r' to 'b' or vice-versa
        self.current_player = 'b' if self.current_player == 'r' else 'r'
    def has_any_valid_moves(self, player=None):
        # Check if player has *any* legal move
        if player is None:
            player = self.current_player
        for sr in range(8):
            for sc in range(8):
                if self.is_own_piece(sr, sc, player):
                    # Check simple moves
                    for dr, dc in self.get_allowed_directions(self.board[sr][sc]):
                        er = sr + dr
                        ec = sc + dc
                        if self.is_valid_normal_move(sr, sc, er, ec):
                            return True
                    # Check capture moves
                    for dr, dc in self.get_all_directions():
                        er = sr + 2 * dr
                        ec = sc + 2 * dc
                        if self.is_valid_capture_move(sr, sc, er, ec):
                            return True
        return False
    def process_move(self, sr, sc, er, ec):
        # Full move executor: validates move, applies it, switches turn
        # 1. Check board boundaries
        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False, "out_of_bounds", self.current_player
        # 2. Ensure player is selecting their own piece
        if not self.is_own_piece(sr, sc):
            return False, "Not your piece", self.current_player
        # 3. Check mandatory capture rule
        captures = self.get_all_captures()
        capture_mode = len(captures) > 0
        if capture_mode:
            # Capture must move exactly 2 squares in both directions
            if (er - sr) % 2 != 0 or (ec - sc) % 2 != 0:
                return False, "You must capture!", self.current_player
            # Validate capture move
            if not self.is_valid_capture_move(sr, sc, er, ec):
                return False, "Invalid capture move", self.current_player
            # Apply capture
            self.apply_capture_move(sr, sc, er, ec)
            # Check for multi-capture
            if self.has_more_captures(er, ec):
                return True, "Continue capturing", self.current_player
            # Promote after final capture
            self.promote_to_king(er, ec)
        else:
            # No capture mode → must be normal move
            if not self.is_valid_normal_move(sr, sc, er, ec):
                return False, "Invalid move", self.current_player
            self.apply_normal_move(sr, sc, er, ec)
        # After completing move, switch turn
        self.switch_player()
        return True, "Move successful", self.current_player
    def debug_square(self, r, c):
        print(f"({r},{c}) -> {self.board[r][c]}")
    def get_all_valid_moves(self, player=None):
        # Return dictionary of ALL legal moves for this player
        if player is None:
            player = self.current_player.lower()
        normal_moves = {}
        capture_moves = {}
        for sr in range(8):
            for sc in range(8):
                if not self.is_own_piece(sr, sc, player):
                    continue
                piece = self.board[sr][sc]
                # Simple 1-step moves
                directions = self.get_allowed_directions(piece)
                for dr, dc in directions:
                    er = sr + dr
                    ec = sc + dc
                    if self.is_valid_normal_move(sr, sc, er, ec):
                        normal_moves.setdefault((sr, sc), []).append((er, ec))
                # Capture moves (2 steps)
                for dr, dc in self.get_all_directions():
                    er = sr + 2 * dr
                    ec = sc + 2 * dc
                    if self.is_valid_capture_move(sr, sc, er, ec):
                        capture_moves.setdefault((sr, sc), []).append((er, ec))
# If any capture exists → mandatory capture rule
        if capture_moves:
            return capture_moves
        return normal_moves