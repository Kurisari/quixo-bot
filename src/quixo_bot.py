from tabulate import tabulate

class QuixoBot:
    
    ALLOWED_PIECES_RIGHT = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]
    ALLOWED_PIECES_LEFT = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4), (4, 4), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_UP = [(1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_DOWN = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4)]
    ALLOWED_PIECES_GENERAL = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 1 if symbol == -1 else -1
        self.board = [[0] * 5 for _ in range(5)]
    
    def play_turn(self, board):
        _, move = self.minimax(board, 3, True)  # Profundidad 3 para ejemplo, puede ajustarse
        print(move)
        if move:
            direction, (row, col) = move
            if direction == 'right':
                self.move_right(board, row, col)
            elif direction == 'left':
                self.move_left(board, row, col)
            elif direction == 'up':
                self.move_up(board, row, col)
            elif direction == 'down':
                self.move_down(board, row, col)
        return board
    
    def move_right(self, board, row, col, end_col=4):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_RIGHT:
            if piece == 0 or piece == self.symbol:
                for i in range(col, end_col):
                    board[row][i] = board[row][i + 1]
                board[row][end_col] = self.symbol
    
    def move_left(self, board, row, col, end_col=0):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_LEFT:
            if piece == 0 or piece == self.symbol:
                for i in range(col, end_col, -1):
                    board[row][i] = board[row][i - 1]
                board[row][end_col] = self.symbol
    
    def move_up(self, board, row, col, end_row=0):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_UP:
            if piece == 0 or piece == self.symbol:
                for i in range(row, end_row, -1):
                    board[i][col] = board[i - 1][col]
                board[end_row][col] = self.symbol
    
    def move_down(self, board, row, col, end_row=4):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_DOWN:
            if piece == 0 or piece == self.symbol:
                for i in range(row, end_row):
                    board[i][col] = board[i + 1][col]
                board[end_row][col] = self.symbol
    
    def print_board(self, board=None):
        if board is None:
            board = self.board
        headers = [""] + [str(i) for i in range(1, 6)]
        rows = [[str(i + 1)] + ['O' if cell == -1 else 'X' if cell == 1 else ' ' for cell in row] for i, row in enumerate(board)]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def reset(self):
        pass

    def is_winner(self, board, symbol):
        lines = []
        for i in range(5):
            lines.append(board[i])
            lines.append([board[j][i] for j in range(5)])
        lines.append([board[i][i] for i in range(5)])
        lines.append([board[i][4 - i] for i in range(5)])
        for line in lines:
            if all(cell == symbol for cell in line):
                return True
        return False

    def is_full(self, board):
        for row in board:
            if 0 in row:
                return False
        return True

    def evaluate(self, board):
        if self.is_winner(board, self.symbol):
            return 1
        elif self.is_winner(board, self.opponent_symbol):
            return -1
        else:
            return 0

    def minimax(self, board, depth, maximizing):
        if self.is_winner(board, self.symbol) or self.is_winner(board, self.opponent_symbol) or depth == 0 or self.is_full(board):
            return self.evaluate(board), None
        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in self.generate_moves(board, self.symbol):
                new_board = self.apply_move(board, move, self.symbol)
                eval = self.minimax(new_board, depth - 1, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.generate_moves(board, self.opponent_symbol):
                new_board = self.apply_move(board, move, self.opponent_symbol)
                eval = self.minimax(new_board, depth - 1, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def generate_moves(self, board, symbol):
        moves = []
        for row, col in self.ALLOWED_PIECES_GENERAL:
            if board[row][col] == 0 or board[row][col] == symbol:
                if (row, col) in self.ALLOWED_PIECES_RIGHT:
                    moves.append(('right', (row, col)))
                if (row, col) in self.ALLOWED_PIECES_LEFT:
                    moves.append(('left', (row, col)))
                if (row, col) in self.ALLOWED_PIECES_UP:
                    moves.append(('up', (row, col)))
                if (row, col) in self.ALLOWED_PIECES_DOWN:
                    moves.append(('down', (row, col)))
        return moves

    def apply_move(self, board, move, symbol):
        new_board = [row[:] for row in board]
        direction, (row, col) = move
        if direction == 'right':
            self.move_right(new_board, row, col)
        elif direction == 'left':
            self.move_left(new_board, row, col)
        elif direction == 'up':
            self.move_up(new_board, row, col)
        elif direction == 'down':
            self.move_down(new_board, row, col)
        return new_board