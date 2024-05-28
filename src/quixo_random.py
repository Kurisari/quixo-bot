from tabulate import tabulate
import random
import copy

class QuixoRandomBot:
    ALLOWED_PIECES_RIGHT = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]
    ALLOWED_PIECES_LEFT = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4), (4, 4), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_UP = [(1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_DOWN = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4)]
    ALLOWED_PIECES_GENERAL = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 1 if symbol == -1 else -1
        self.board = [[0] * 5 for _ in range(5)]
        self.name = "Kuri Bot Random"

    def play_turn(self, board):
        valid_moves = self.generate_moves(board, self.symbol)
        if valid_moves:
            move = random.choice(valid_moves)
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

    def reset(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 1 if symbol == -1 else -1
        self.board = [[0] * 5 for _ in range(5)]

    def is_winner(self, board, symbol):
        lines = [board[i] for i in range(5)] + [[board[j][i] for j in range(5)] for i in range(5)]
        lines.append([board[i][i] for i in range(5)])
        lines.append([board[i][4 - i] for i in range(5)])
        for line in lines:
            if all(cell == symbol for cell in line):
                return True
        return False

    def is_full(self, board):
        return all(cell != 0 for row in board for cell in row)

    def generate_moves(self, board, symbol):
        moves = []
        allowed_positions = self.ALLOWED_PIECES_GENERAL
        for direction in ['right', 'left', 'up', 'down']:
            for row, col in allowed_positions:
                if board[row][col] == 0 or board[row][col] == symbol:
                    if self.is_valid_move(board, direction, row, col, symbol):
                        moves.append((direction, (row, col)))
        return moves

    def is_valid_move(self, board, direction, row, col, symbol):
        if direction == 'right' and col < 4 and (board[row][col + 1] == 0 or board[row][col + 1] == symbol):
            return True
        if direction == 'left' and col > 0 and (board[row][col - 1] == 0 or board[row][col - 1] == symbol):
            return True
        if direction == 'up' and row > 0 and (board[row - 1][col] == 0 or board[row - 1][col] == symbol):
            return True
        if direction == 'down' and row < 4 and (board[row + 1][col] == 0 or board[row + 1][col] == symbol):
            return True
        return False

    def apply_move(self, board, move, symbol):
        new_board = copy.deepcopy(board)
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
