class gamelogicin :
    def __init__(self,board,current_player):
        self.board=board
        self.current_player=current_player
    def is_own_piece(self,row,col):
        piece = self.board[row][col]
        if piece == ".":
            return False
        if self.current_player == "r":
            return piece in ["r","R"]
        # r = red piece , R = Red king
        else:
            return piece in ["b","B"]
        # b = balck piece , B = Black king
    def get_allowed_directions(self,piece):
        if piece in ["R","B"]:
            return [(1,1),(1,-1),(-1,1),(-1,-1)]
        if piece=="r":
            return [(-1,-1),(-1,1)]
        if piece=="b":
            return [(1,-1),(1,1)]
    def get_all_captures(self):
        capture=[]
        for row in range(8):
            for col in range(8):
                if not self.is_own_piece(row,col):
                    continue
                piece = self.board[row][col]
                if self.has_capture_from(row,col,piece):
                    capture.append((row,col))
        return capture
    def _has_capture_from(self,r,c,piece):
        directions = self.get_all_directions(piece)
        for dr , dc in directions:
            mid_r = r+dr
            mid_c = c+dc
            end_r = r + 2*dr
            end_c = c + 2*dc
            if 0 <= mid_r < 8 and 0 <= mid_c < 8 and 0 <= end_r < 8 and 0 <= end_c < 8:
                middle_piece = self.board[mid_r][mid_c]
                destination = self.board[end_r][end_c]
                if self.is_opponent_piece(middle_piece) and destination == ".":
                    return True
        return False
    def _is_opponent_player(self,piece):
        if piece == ".":
            return False
        if self.current_player == "r":
            return piece in ["b","B"]
        else:
            return piece in ["r","R"]
    def is_vaild_normal_move(self,sr,sc,er,ec):
        if self.board[er][ec] != ".":
            return False
        piece= self.board[sr][sc]
        directions = self.get_allowed_directions(piece)
        for dr,dc in directions:
            if er==sr+dr and ec==sc+dc:
                return True
        return False
    def is_valid_capture_move(self,sr,sc,er,ec):
        piece = self.board[sr][sc]
        directions = self.get_allowed_directions(piece)
        for dr , dc in directions:
            mid_r = sr+dr
            mid_c = sc+dc
            end_r = sr + 2* dr
            end_c = sc + 2* dc
            if er==end_r and ec==end_c:
                if(0 <= mid_r < 8 and 0 <= mid_c <8 and self._is_opponent_piece(self.board[mid_r][mid_c]) and self.board[er][ec]=="."):
                    return True
        return False
    def apply_normal_move(self,sr,sc,er,ec):
        piece = self.board[sr][sc]
        self.board[sr][sc]= "."
        self.board[er][ec]= piece
    def apply_capture_move(self,sr,sc,er,ec):
        piece= self.board[sr][sc]
        dr = (er - sr ) //  2
        dc = (ec - sc ) // 2
        mid_r = sr + dr
        mid_c = sc + dc
        self.board[mid_r][mid_c]="."
        self.board[sr][sc]="."
        self.board[er][ec]=piece
    def has_more_captures(self, r, c):
        piece = self.board[r][c]
        return self._has_capture_from(r, c, piece)
    def promote_to_king(self, r, c):
        piece = self.board[r][c]
        if piece == "r" and r == 0:
            self.board[r][c] = "R"
        elif piece == "b" and r == 7:
            self.board[r][c] = "B"
    def process_move(self, sr, sc, er, ec):
        if not self.is_own_piece(sr, sc):
            return False, "Not your piece"
        piece = self.board[sr][sc]
        mandatory_captures = self.get_all_captures()
        if mandatory_captures and (sr, sc) not in mandatory_captures:
            return False, "You must capture!"
        if self.is_valid_capture_move(sr, sc, er, ec):
            self.apply_capture_move(sr, sc, er, ec)
            if self.has_more_captures(er, ec):
                return True, "Continue capturing"
        elif not mandatory_captures and self.is_valid_normal_move(sr, sc, er, ec):
            self.apply_normal_move(sr, sc, er, ec)
        else:
            return False, "Invalid move"
        self.promote_to_king(er, ec)
        self.switch_player()
        return True, "Move successful"
    def switch_player(self):
        self.current_player = "b" if self.current_player == "r" else "r"