import os
import sys
from tabulate import tabulate

script_dir = os.getcwd()
func_dir = os.path.join(script_dir)
sys.path.append(func_dir)

from lib import quixo_lib as ql

class QuixoBot:
    
    ALLOWED_PIECES_RIGHT = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]
    ALLOWED_PIECES_LEFT = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4), (4, 4), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_UP = [(1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_DOWN = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4)]
    ALLOWED_PIECES_GENERAL = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.board = [[0] * 5 for _ in range(5)]
    
    def play_turn(self, board=None):
        if board is None:
            board = self.board
    
    def move_right(self, board, row, col, end_col=4):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_RIGHT and self.validate_move(board, row, col):
            if piece == 0 or piece == self.symbol:
                for i in range(col, end_col + 1):
                    board[row][i] = board[row][i + 1] if i != 4 else self.symbol
            self.print_board()
        else:
            print("Invalid move")
    
    def move_left(self, board, row, col, end_col=0):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_LEFT and self.validate_move(board, row, col):
            if piece == 0 or piece == self.symbol:
                for i in range(col, end_col - 1, -1):
                    board[row][i] = board[row][i - 1] if i != 0 else self.symbol
            self.print_board()
        else:
            print("Invalid move")
    
    def move_up(self, board, row, col, end_row=0):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_UP and self.validate_move(board, row, col):
            if piece == 0 or piece == self.symbol:
                for i in range(row, end_row - 1, -1):
                    board[i][col] = board[i - 1][col] if i != 0 else self.symbol
            self.print_board()
        else:
            print("Invalid move")
    
    def move_down(self, board, row, col, end_row=4):
        piece = board[row][col]
        if (row, col) in self.ALLOWED_PIECES_DOWN and self.validate_move(board, row, col):
            if piece == 0 or piece == self.symbol:
                for i in range(row, end_row + 1):
                    board[i][col] = board[i + 1][col] if i != 4 else self.symbol
            self.print_board()
        else:
            print("Invalid move")
    
    def print_board(self):
        headers = [""] + [str(i) for i in range(1, 6)]
        rows = [[str(i + 1)] + ['O' if cell == 1 else 'X' if cell == 2 else ' ' for cell in row] for i, row in enumerate(self.board)]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def reset(self):
        pass
    
    def validate_move(self, board, row, col):
        if (row, col) in self.ALLOWED_PIECES_GENERAL:
            return True
        return False

prueba = QuixoBot(1)
prueba.play_turn()