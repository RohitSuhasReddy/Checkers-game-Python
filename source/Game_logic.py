EMPTY = ''  # Change to '.' if your board uses '.' for empty squares

class GameLogic:
    def __init__(self, board):
        self.board = board

    def is_valid_move(self, start, end, player):
        """
        Validates if the given move is allowed.
        start, end are (row, col) tuples.
        Returns (True, "reason") or (False, "reason").
        """
        sr, sc = start
        er, ec = end

        # Out of bounds check
        if not (0 <= sr < len(self.board) and 0 <= sc < len(self.board[0]) and
                0 <= er < len(self.board) and 0 <= ec < len(self.board[0])):
            return False, "out_of_bounds"

        start_piece = self.board[sr][sc]
        dest_piece = self.board[er][ec]

        if start_piece == EMPTY:
            return False, "no_piece_at_start"
        if dest_piece != EMPTY:
            return False, "destination_not_empty"

        # Make sure the piece belongs to the player
        if start_piece.lower() != player.lower():
            return False, "not_your_piece"

        dr = er - sr  # row difference
        dc = ec - sc  # column difference

        # Determine forward direction
        # Red moves UP (row decreases), Black moves DOWN (row increases)
        forward = -1 if player.lower() == 'r' else 1

        # Simple move (1 step diagonally)
        if abs(dr) == 1 and abs(dc) == 1:
            # Men (non-king pieces) move only forward
            if start_piece in ('r', 'b'):
                if dr != forward:
                    return False, "wrong_direction_for_man"
            return True, "simple_ok"

        # Jump move (2 steps diagonally)
        if abs(dr) == 2 and abs(dc) == 2:
            mid_row = (sr + er) // 2
            mid_col = (sc + ec) // 2
            mid_piece = self.board[mid_row][mid_col]

            if mid_piece == EMPTY:
                return False, "no_piece_to_capture"
            if mid_piece.lower() == start_piece.lower():
                return False, "cannot_capture_own_piece"

            # Direction check for men
            if start_piece in ('r', 'b'):
                if dr != 2 * forward:
                    return False, "wrong_direction_for_man_capture"

            return True, "capture_ok"

        return False, "not_a_valid_diagonal_move"

    def move_piece(self, start, end):
        """Performs the move and removes captured piece if it's a jump."""
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]

        # If it's a jump (capture), remove the middle piece
        if abs(er - sr) == 2 and abs(ec - sc) == 2:
            mid_row = (sr + er) // 2
            mid_col = (sc + ec) // 2
            self.board[mid_row][mid_col] = EMPTY  # remove captured piece

        # Move the piece
        self.board[er][ec] = piece
        self.board[sr][sc] = EMPTY

        # Promotion to king
        if piece == 'r' and er == 0:
            self.board[er][ec] = 'R'
        elif piece == 'b' and er == len(self.board) - 1:
            self.board[er][ec] = 'B'

    def debug_square(self, r, c):
        """Helper to print what's on a square (for debugging)."""
        if 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
            print(f"DEBUG ({r},{c}) = {repr(self.board[r][c])}")
        else:
            print(f"DEBUG ({r},{c}) is out of bounds")