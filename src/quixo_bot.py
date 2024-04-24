import os
import sys
from tabulate import tabulate

script_dir = os.getcwd()
func_dir = os.path.join(script_dir)
sys.path.append(func_dir)

from lib import quixo_lib as ql

class QuixoBot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.board = [[0] * 5 for _ in range(5)]
    
    def play_turn(self, board):
        pass
    
    def __move_right(self, board, row, col, end_col=4):
        pass
    
    def __move_left(self, board, row, col, end_col=0):
        pass
    
    def __move_up(self, board, row, col, end_row=0):
        pass
    
    def __move_down(self, board, row, col, end_row=4):
        pass
    
    def print_board(self):
        headers = [""] + [str(i) for i in range(1, 6)]
        rows = [[str(i + 1)] + ['O' if cell == 1 else 'X' if cell == 2 else ' ' for cell in row] for i, row in enumerate(self.board)]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def reset(self):
        pass

prueba = QuixoBot(1)
prueba.print_board()