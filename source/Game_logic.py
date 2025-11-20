

EMPTY = "."

class GameLogic:
    def __init__(self, board, current_player='r'):
        self.board = board
        self.current_player = current_player  # 'r' or 'b'

    # -------------------------------------------------------
    # Helper: Check inside
    # -------------------------------------------------------
    def is_inside(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    # -------------------------------------------------------
    # Identification helpers
    # -------------------------------------------------------
    def is_own_piece(self, r, c, player=None):
        if player is None:
            player = self.current_player

        if not self.is_inside(r, c):
            return False

        piece = self.board[r][c]
        if piece == EMPTY:
            return False

        return piece.lower() == player.lower()

    def _is_opponent_player(self, r, c, player):
        if not self.is_inside(r, c):
            return False

        piece = self.board[r][c]
        if piece == EMPTY:
            return False

        return piece.lower() != player.lower()

    # -------------------------------------------------------
    # Movement directions
    # -------------------------------------------------------
    def get_allowed_directions(self, piece):
        if piece in ("R", "B"):  # kings
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece == "r":  # red moves up
            return [(-1, -1), (-1, 1)]
        if piece == "b":  # black moves down
            return [(1, -1), (1, 1)]
        return []

    def get_all_directions(self):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    # -------------------------------------------------------
    # Normal move validation
    # -------------------------------------------------------
    def is_valid_normal_move(self, sr, sc, er, ec):
        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False

        piece = self.board[sr][sc]
        if piece == EMPTY:
            return False

        if self.board[er][ec] != EMPTY:
            return False

        dr = er - sr
        dc = ec - sc

        if abs(dr) != 1 or abs(dc) != 1:
            return False

        if piece in ("r", "b"):
            forward = -1 if piece == "r" else 1
            if dr != forward:
                return False

        return True

    # -------------------------------------------------------
    # Capture move validation
    # -------------------------------------------------------
    def is_valid_capture_move(self, sr, sc, er, ec):
        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False

        piece = self.board[sr][sc]
        if piece == EMPTY:
            return False

        if self.board[er][ec] != EMPTY:
            return False

        dr = er - sr
        dc = ec - sc

        if abs(dr) != 2 or abs(dc) != 2:
            return False

        mid_r = sr + dr // 2
        mid_c = sc + dc // 2

        if not self.is_inside(mid_r, mid_c):
            return False

        if not self._is_opponent_player(mid_r, mid_c, piece):
            return False

        if piece in ("r", "b"):
            forward = -1 if piece == "r" else 1
            if dr != 2 * forward:
                return False

        return True

    # -------------------------------------------------------
    # Has capture from square?
    # -------------------------------------------------------
    def _has_capture_from(self, r, c):
        piece = self.board[r][c]
        if piece == EMPTY:
            return False

        for dr, dc in self.get_all_directions():
            er = r + 2*dr
            ec = c + 2*dc
            if self.is_valid_capture_move(r, c, er, ec):
                return True
        return False

    # -------------------------------------------------------
    # Get all captures on board for current player
    # -------------------------------------------------------
    def get_all_captures(self):
        captures = {}
        for r in range(8):
            for c in range(8):
                if self.is_own_piece(r, c):
                    piece_moves = []
                    for dr, dc in self.get_all_directions():
                        er = r + 2*dr
                        ec = c + 2*dc
                        if self.is_valid_capture_move(r, c, er, ec):
                            piece_moves.append((er, ec))
                    if piece_moves:
                        captures[(r, c)] = piece_moves

        return captures

    # -------------------------------------------------------
    # Apply normal move
    # -------------------------------------------------------
    def apply_normal_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]
        self.board[sr][sc] = EMPTY
        self.board[er][ec] = piece

        self.promote_to_king(er, ec)

    # -------------------------------------------------------
    # Apply capture move
    # -------------------------------------------------------
    def apply_capture_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]

        mid_r = (sr + er) // 2
        mid_c = (sc + ec) // 2

        self.board[mid_r][mid_c] = EMPTY
        self.board[sr][sc] = EMPTY
        self.board[er][ec] = piece

        self.promote_to_king(er, ec)

    # -------------------------------------------------------
    # Check for multi-capture possibility
    # -------------------------------------------------------
    def has_more_captures(self, r, c):
        return self._has_capture_from(r, c)

    # -------------------------------------------------------
    # Promotion
    # -------------------------------------------------------
    def promote_to_king(self, r, c):
        piece = self.board[r][c]
        if piece == "r" and r == 0:
            self.board[r][c] = "R"
        elif piece == "b" and r == 7:
            self.board[r][c] = "B"

    # -------------------------------------------------------
    # Switch player
    # -------------------------------------------------------
    def switch_player(self):
        self.current_player = 'b' if self.current_player == 'r' else 'r'

    # -------------------------------------------------------
    # Check if player has any moves
    # -------------------------------------------------------
    def has_any_valid_moves(self, player=None):
        if player is None:
            player = self.current_player

        for sr in range(8):
            for sc in range(8):
                if self.is_own_piece(sr, sc, player):
                    for dr, dc in self.get_allowed_directions(self.board[sr][sc]):
                        er = sr + dr
                        ec = sc + dc
                        if self.is_valid_normal_move(sr, sc, er, ec):
                            return True

                    for dr, dc in self.get_all_directions():
                        er = sr + 2*dr
                        ec = sc + 2*dc
                        if self.is_valid_capture_move(sr, sc, er, ec):
                            return True

        return False

    # -------------------------------------------------------
    # PROCESS MOVE (MAIN FUNCTION)
    # -------------------------------------------------------
    def process_move(self, sr, sc, er, ec):

        if not (self.is_inside(sr, sc) and self.is_inside(er, ec)):
            return False, "out_of_bounds", self.current_player

        if not self.is_own_piece(sr, sc):
            return False, "Not your piece", self.current_player

        captures = self.get_all_captures()
        capture_mode = len(captures) > 0

        if capture_mode:
            if (er - sr) % 2 != 0 or (ec - sc) % 2 != 0:
                return False, "You must capture!", self.current_player
            if not self.is_valid_capture_move(sr, sc, er, ec):
                return False, "Invalid capture move", self.current_player

            self.apply_capture_move(sr, sc, er, ec)

            if self.has_more_captures(er, ec):
                return True, "Continue capturing", self.current_player

        else:
            if not self.is_valid_normal_move(sr, sc, er, ec):
                return False, "Invalid move", self.current_player
            self.apply_normal_move(sr, sc, er, ec)

        self.switch_player()
        return True, "Move successful", self.current_player

    # -------------------------------------------------------
    # DEBUG HELPER
    # -------------------------------------------------------
    def debug_square(self, r, c):
        print(f"({r},{c}) -> {self.board[r][c]}")

    # -------------------------------------------------------
    # ⭐ ADDITION: get_all_valid_moves
    # -------------------------------------------------------
    def get_all_valid_moves(self, player=None):
        """
        Returns ALL legal moves for the player in dict form.
        Mandatory capture rule applied.
        {
            (sr,sc): [(er,ec), (er2,ec2), ...],
            ...
        }
        """

        if player is None:
            player = self.current_player.lower()

        normal_moves = {}
        capture_moves = {}

        for sr in range(8):
            for sc in range(8):
                if not self.is_own_piece(sr, sc, player):
                    continue

                piece = self.board[sr][sc]
                directions = self.get_allowed_directions(piece)

                # Simple moves
                for dr, dc in directions:
                    er = sr + dr
                    ec = sc + dc
                    if self.is_valid_normal_move(sr, sc, er, ec):
                        normal_moves.setdefault((sr, sc), []).append((er, ec))

                # Capture moves
                for dr, dc in self.get_all_directions():
                    er = sr + 2*dr
                    ec = sc + 2*dc
                    if self.is_valid_capture_move(sr, sc, er, ec):
                        capture_moves.setdefault((sr, sc), []).append((er, ec))

        if capture_moves:
            return capture_moves

        return normal_moves