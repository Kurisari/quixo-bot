import numpy as np
import random
from tabulate import tabulate

class QuixoBotQLearning:
    def __init__(self, symbol, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.symbol = symbol
        self.opponent_symbol = 1 if symbol == -1 else -1
        self.board = np.zeros((5, 5), dtype=int)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}  # Q-Table para almacenar los valores Q

    def play_turn(self, board):
        state = self.board_to_state(board)
        if random.uniform(0, 1) < self.epsilon:
            # Exploración: elegir una acción aleatoria
            move = self.get_random_move(board)
        else:
            # Explotación: elegir la mejor acción conocida
            move = self.get_best_move(state)
        
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

        new_state = self.board_to_state(board)
        reward = self.get_reward(board)
        self.update_q_table(state, move, new_state, reward)

        return board

    def get_random_move(self, board):
        allowed_positions = self.get_allowed_positions()
        moves = []
        for direction in ['right', 'left', 'up', 'down']:
            for row, col in allowed_positions:
                if board[row][col] == 0 or board[row][col] == self.symbol:
                    if self.is_valid_move(board, direction, row, col):
                        moves.append((direction, (row, col)))
        return random.choice(moves) if moves else None

    def get_best_move(self, state):
        if state not in self.q_table or not self.q_table[state]:
            return self.get_random_move(self.board)
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_table(self, state, action, new_state, reward):
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0
        future_rewards = 0
        if new_state in self.q_table:
            future_rewards = max(self.q_table[new_state].values())
        self.q_table[state][action] += self.alpha * (reward + self.gamma * future_rewards - self.q_table[state][action])

    def board_to_state(self, board):
        return tuple(map(tuple, board))

    def get_reward(self, board):
        if self.is_winner(board, self.symbol):
            return 1
        elif self.is_winner(board, self.opponent_symbol):
            return -1
        else:
            return 0

    def get_allowed_positions(self):
        return [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 4), (2, 0), (2, 4), (3, 0), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

    def move_right(self, board, row, col, end_col=4):
        piece = board[row][col]
        if piece == 0 or piece == self.symbol:
            for i in range(col, end_col):
                board[row][i] = board[row][i + 1]
            board[row][end_col] = self.symbol

    def move_left(self, board, row, col, end_col=0):
        piece = board[row][col]
        if piece == 0 or piece == self.symbol:
            for i in range(col, end_col, -1):
                board[row][i] = board[row][i - 1]
            board[row][end_col] = self.symbol

    def move_up(self, board, row, col, end_row=0):
        piece = board[row][col]
        if piece == 0 or piece == self.symbol:
            for i in range(row, end_row, -1):
                board[i][col] = board[i - 1][col]
            board[end_row][col] = self.symbol

    def move_down(self, board, row, col, end_row=4):
        piece = board[row][col]
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
        self.board = np.zeros((5, 5), dtype=int)

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

    def is_valid_move(self, board, direction, row, col):
        if direction == 'right' and col < 4 and (board[row][col + 1] == 0 or board[row][col + 1] == self.symbol):
            return True
        if direction == 'left' and col > 0 and (board[row][col - 1] == 0 or board[row][col - 1] == self.symbol):
            return True
        if direction == 'up' and row > 0 and (board[row - 1][col] == 0 or board[row - 1][col] == self.symbol):
            return True
        if direction == 'down' and row < 4 and (board[row + 1][col] == 0 or board[row + 1][col] == self.symbol):
            return True
        return False