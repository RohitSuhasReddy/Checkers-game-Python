class GameLogic:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player

    # ---------------------------
    # BASIC HELPERS
    # ---------------------------
    def is_own_piece(self, row, col):
        piece = self.board[row][col]
        if piece == ".":
            return False

        if self.current_player == "r":
            return piece in ["r", "R"]   # red normal + king
        else:
            return piece in ["b", "B"]   # black normal + king

    def _is_opponent_player(self, piece):
        if piece == ".":
            return False

        if self.current_player == "r":
            return piece in ["b", "B"]
        else:
            return piece in ["r", "R"]

    # ---------------------------
    # MOVEMENT RULES
    # ---------------------------
    def get_allowed_directions(self, piece):
        if piece in ["R", "B"]:  # kings
            return [(1,1), (1,-1), (-1,1), (-1,-1)]

        if piece == "r":
            return [(-1,-1), (-1,1)]     # red moves up
        if piece == "b":
            return [(1,-1), (1,1)]       # black moves down

    # NEW FIXED FUNCTION
    def get_all_directions(self, piece):
        """Used for checking captures. Same as allowed directions."""
        return self.get_allowed_directions(piece)

    # ---------------------------
    # CAPTURE CHECK
    # ---------------------------
    def _has_capture_from(self, r, c, piece):
        directions = self.get_all_directions(piece)

        for dr, dc in directions:
            mid_r = r + dr
            mid_c = c + dc
            end_r = r + 2*dr
            end_c = c + 2*dc

            if 0 <= mid_r < 8 and 0 <= mid_c < 8 and 0 <= end_r < 8 and 0 <= end_c < 8:
                middle_piece = self.board[mid_r][mid_c]
                destination = self.board[end_r][end_c]

                if self._is_opponent_player(middle_piece) and destination == ".":
                    return True

        return False

    def get_all_captures(self):
        capture_list = []

        for row in range(8):
            for col in range(8):
                if not self.is_own_piece(row, col):
                    continue

                piece = self.board[row][col]

                if self._has_capture_from(row, col, piece):
                    capture_list.append((row, col))

        return capture_list

    # ---------------------------
    # MOVE VALIDATION
    # ---------------------------
    def is_valid_normal_move(self, sr, sc, er, ec):
        if self.board[er][ec] != ".":
            return False

        piece = self.board[sr][sc]
        directions = self.get_allowed_directions(piece)

        for dr, dc in directions:
            if er == sr + dr and ec == sc + dc:
                return True

        return False

    def is_valid_capture_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]
        directions = self.get_allowed_directions(piece)

        for dr, dc in directions:
            mid_r = sr + dr
            mid_c = sc + dc
            end_r = sr + 2*dr
            end_c = sc + 2*dc

            if er == end_r and ec == end_c:
                if (0 <= mid_r < 8 and 0 <= mid_c < 8 and
                    self._is_opponent_player(self.board[mid_r][mid_c]) and
                    self.board[er][ec] == "."):
                    return True

        return False

    # ---------------------------
    # APPLY MOVES
    # ---------------------------
    def apply_normal_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]
        self.board[sr][sc] = "."
        self.board[er][ec] = piece

    def apply_capture_move(self, sr, sc, er, ec):
        piece = self.board[sr][sc]
        dr = (er - sr) // 2
        dc = (ec - sc) // 2

        mid_r = sr + dr
        mid_c = sc + dc

        self.board[mid_r][mid_c] = "."
        self.board[sr][sc] = "."
        self.board[er][ec] = piece

    def has_more_captures(self, r, c):
        piece = self.board[r][c]
        return self._has_capture_from(r, c, piece)

    # ---------------------------
    # KING PROMOTION
    # ---------------------------
    def promote_to_king(self, r, c):
        piece = self.board[r][c]

        if piece == "r" and r == 0:
            self.board[r][c] = "R"
        elif piece == "b" and r == 7:
            self.board[r][c] = "B"

    # ---------------------------
    # PROCESS MOVE
    # ---------------------------
    def process_move(self, sr, sc, er, ec):

        if not self.is_own_piece(sr, sc):
            return False, "Not your piece"

        piece = self.board[sr][sc]
        mandatory_captures = self.get_all_captures()

        if mandatory_captures and (sr, sc) not in mandatory_captures:
            return False, "You must capture!"

        # capture move
        if self.is_valid_capture_move(sr, sc, er, ec):
            self.apply_capture_move(sr, sc, er, ec)

            if self.has_more_captures(er, ec):
                return True, "Continue capturing"

        # normal move
        elif not mandatory_captures and self.is_valid_normal_move(sr, sc, er, ec):
            self.apply_normal_move(sr, sc, er, ec)

        else:
            return False, "Invalid move"

        self.promote_to_king(er, ec)
        self.switch_player()

        return True, "Move successful"

    def switch_player(self):
        self.current_player = "b" if self.current_player == "r" else "r"
