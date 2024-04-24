import os
import sys

script_dir = os.getcwd()
func_dir = os.path.join(script_dir)
sys.path.append(func_dir)

from lib import quixo_lib as ql

class QuixoBot:
    def __init__(self, symbol):
        pass
    
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
    
    def __print_board(self):
        pass
    
    def reset(self):
        pass