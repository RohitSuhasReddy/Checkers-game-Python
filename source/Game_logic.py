EMPTY = '.'  # board empty square marker

class GameLogic:
    def __init__(self, board, current_player='r'):
        """
        board: 8x8 list of lists using: 'r','R' (red, red-king), 'b','B' (black,black-king), '.' empty
        current_player: 'r' or 'b'
        """
        self.board = board
        self.current_player = current_player

    # ---- basic helpers ----
    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def is_own_piece(self, r, c):
        piece = self.board[r][c]
        if piece == EMPTY:
            return False
        if self.current_player == 'r':
            return piece in ('r', 'R')
        return piece in ('b', 'B')

    def is_opponent_piece(self, piece):
        if piece == EMPTY:
            return False
        if self.current_player == 'r':
            return piece in ('b', 'B')
        return piece in ('r', 'R')

    def get_allowed_directions(self, piece):
        """Return list of (dr,dc) allowed for that piece (including kings)."""
        if piece in ('R', 'B'):  # kings move both directions
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece == 'r':  # red moves up (row decreases)
            return [(-1, -1), (-1, 1)]
        if piece == 'b':  # black moves down (row increases)
            return [(1, -1), (1, 1)]
        return []

    # ---- capture detection ----
    def _has_capture_from(self, r, c):
        """Check whether piece at (r,c) has at least one capture."""
        piece = self.board[r][c]
        if piece == EMPTY:
            return False
        for dr, dc in self.get_allowed_directions(piece):
            mid_r, mid_c = r + dr, c + dc
            end_r, end_c = r + 2*dr, c + 2*dc
            if self.in_bounds(mid_r, mid_c) and self.in_bounds(end_r, end_c):
                if self.is_opponent_piece(self.board[mid_r][mid_c]) and self.board[end_r][end_c] == EMPTY:
                    return True
        return False

    def get_all_captures(self):
        """Return list of (r,c) coordinates of own pieces that can capture."""
        captures = []
        for r in range(8):
            for c in range(8):
                if self.is_own_piece(r, c) and self._has_capture_from(r, c):
                    captures.append((r, c))
        return captures

    # ---- move validation ----
    def is_valid_normal_move(self, sr, sc, er, ec):
        """Validate a simple (non-capturing) diagonal move of one step."""
        if not (self.in_bounds(sr, sc) and self.in_bounds(er, ec)):
            return False
        if self.board[er][ec] != EMPTY:
            return False
        piece = self.board[sr][sc]
        if piece == EMPTY:
            return False
        for dr, dc in self.get_allowed_directions(piece):
            if er == sr + dr and ec == sc + dc:
                return True
        return False

    def is_valid_capture_move(self, sr, sc, er, ec):
        """Validate capturing jump of two diagonal steps."""
        if not (self.in_bounds(sr, sc) and self.in_bounds(er, ec)):
            return False
        if self.board[er][ec] != EMPTY:
            return False
        piece = self.board[sr][sc]
        if piece == EMPTY:
            return False
        for dr, dc in self.get_allowed_directions(piece):
            mid_r, mid_c = sr + dr, sc + dc
            end_r, end_c = sr + 2*dr, sc + 2*dc
            if er == end_r and ec == end_c:
                if self.in_bounds(mid_r, mid_c) and self.is_opponent_piece(self.board[mid_r][mid_c]):
                    return True
        return False

    # ---- apply moves ----
    def apply_normal_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]
        self.board[sr][sc] = EMPTY
        self.board[er][ec] = piece

    def apply_capture_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]
        # middle square
        mid_r = (sr + er) // 2
        mid_c = (sc + ec) // 2
        self.board[mid_r][mid_c] = EMPTY
        self.board[sr][sc] = EMPTY
        self.board[er][ec] = piece

    def has_more_captures(self, r, c):
        """After a capture landed at (r,c), check if that piece can capture again."""
        return self._has_capture_from(r, c)

    def promote_to_king(self, r, c):
        piece = self.board[r][c]
        if piece == 'r' and r == 0:
            self.board[r][c] = 'R'
        elif piece == 'b' and r == 7:
            self.board[r][c] = 'B'

    # ---- game-level helpers ----
    def switch_player(self):
        self.current_player = 'b' if self.current_player == 'r' else 'r'

    def has_any_valid_moves(self, player=None):
        """Check whether the specified player (or current_player if None) has any legal move."""
        saved_player = None
        if player is not None:
            saved_player = self.current_player
            self.current_player = player

        # If any piece has a capture -> there is a move
        if self.get_all_captures():
            if saved_player is not None:
                self.current_player = saved_player
            return True

        # Otherwise check simple moves
        for r in range(8):
            for c in range(8):
                if self.is_own_piece(r, c):
                    piece = self.board[r][c]
                    for dr, dc in self.get_allowed_directions(piece):
                        er, ec = r + dr, c + dc
                        if self.in_bounds(er, ec) and self.board[er][ec] == EMPTY:
                            if saved_player is not None:
                                self.current_player = saved_player
                            return True

        if saved_player is not None:
            self.current_player = saved_player
        return False

    # ---- single public entry to process a move ----
    def process_move(self, sr, sc, er, ec):
        """
        Attempt move from (sr,sc) -> (er,ec).
        Returns: (success: bool, message: str)
        Messages: "Not your piece", "You must capture!", "Continue capturing", "Move successful", "Invalid move"
        """
        # basic checks
        if not self.in_bounds(sr, sc) or not self.in_bounds(er, ec):
            return False, "out_of_bounds"

        if not self.is_own_piece(sr, sc):
            return False, "Not your piece"

        piece = self.board[sr][sc]
        mandatory_captures = self.get_all_captures()

        # If there are mandatory captures, you must use one of the capturing pieces
        if mandatory_captures and (sr, sc) not in mandatory_captures:
            return False, "You must capture!"

        # Try capture first
        if self.is_valid_capture_move(sr, sc, er, ec):
            self.apply_capture_move(sr, sc, er, ec)
            self.promote_to_king(er, ec)
            # if the same piece can capture again, do not switch player
            if self.has_more_captures(er, ec):
                return True, "Continue capturing"
            # otherwise end turn
            self.switch_player()
            return True, "Move successful"

        # If no mandatory captures exist, allow normal move
        if not mandatory_captures and self.is_valid_normal_move(sr, sc, er, ec):
            self.apply_normal_move(sr, sc, er, ec)
            self.promote_to_king(er, ec)
            self.switch_player()
            return True, "Move successful"

        return False, "Invalid move"
