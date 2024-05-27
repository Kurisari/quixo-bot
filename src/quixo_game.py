import os
import sys
from tabulate import tabulate
import time

script_dir = os.getcwd()
func_dir = os.path.join(script_dir)
sys.path.append(func_dir)

import quixo_bot as qb
import quixo2 as q2
import quixo_random as qr
class QuixoGame:
    
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = [[0] * 5 for _ in range(5)]
    
    def check_winner(self, board):
        # Check rows
        for row in board:
            if all(cell == 1 for cell in row):
                return 1
            elif all(cell == -1 for cell in row):
                return -1
        
        # Check columns
        for col in range(5):
            if all(row[col] == 1 for row in board):
                return 1
            elif all(row[col] == -1 for row in board):
                return -1
        
        # Check diagonals
        if all(board[i][i] == 1 for i in range(5)):
            return 1
        elif all(board[i][i] == -1 for i in range(5)):
            return -1
        if all(board[i][4-i] == 1 for i in range(5)):
            return 1
        elif all(board[i][4-i] == -1 for i in range(5)):
            return -1
        
        return 0

    def play_game(self):
        turn = 0
        while True:
            if turn % 2 == 0:
                time1 = time.time()
                self.board = self.player1.play_turn(self.board)
                time2 = time.time()
                print("Time taken: ", time2 - time1)
                self.print_board(self.board)
                winner = self.check_winner(self.board)
                if winner != 0:
                    print("Player", winner, "wins!")
                    break
            else:
                time1 = time.time()
                self.board = self.player2.play_turn(self.board)
                time2 = time.time()
                print("Time taken: ", time2 - time1)
                self.print_board(self.board)
                winner = self.check_winner(self.board)
                if winner != 0:
                    print("Player", winner, "wins!")
                    break
            turn += 1
    
    def print_board(self, board):
        headers = [""] + [str(i) for i in range(1, 6)]
        rows = [[str(i + 1)] + ['O' if cell == -1 else 'X' if cell == 1 else ' ' for cell in row] for i, row in enumerate(self.board)]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

class QuixoHuman:
    
    ALLOWED_PIECES_RIGHT = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]
    ALLOWED_PIECES_LEFT = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4), (4, 4), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_UP = [(1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    ALLOWED_PIECES_DOWN = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4)]
    ALLOWED_PIECES_GENERAL = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    
    def __init__(self, symbol):
        self.symbol = symbol
    
    def play_turn(self, board):
        self.print_board(board)
        print("Enter move: ")
        move = input()
        if move == "q":
            sys.exit()
        row, col, direction = map(int, move.split())
        if direction == 0:
            self.move_up(board, row, col)
        elif direction == 1:
            self.move_down(board, row, col)
        elif direction == 2:
            self.move_left(board, row, col)
        elif direction == 3:
            self.move_right(board, row, col)
    
    def move_right(self, board, row, col):
        qb.QuixoBot.move_right(self, board, row, col)
    
    def move_left(self, board, row, col):
        qb.QuixoBot.move_left(self, board, row, col)
    
    def move_up(self, board, row, col):
        qb.QuixoBot.move_up(self, board, row, col)
    
    def move_down(self, board, row, col):
        qb.QuixoBot.move_down(self, board, row, col)
    
    def print_board(self, board):
        headers = [""] + [str(i) for i in range(1, 6)]
        rows = [[str(i + 1)] + ['O' if cell == -1 else 'X' if cell == 1 else ' ' for cell in row] for i, row in enumerate(board)]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    def validate_move(self, board, row, col):
        if (row, col) in self.ALLOWED_PIECES_GENERAL:
            return True
        return False

prueba = QuixoGame(qb.QuixoBot(1), qr.QuixoRandomBot(-1))
prueba.play_game()