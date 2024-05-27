from tabulate import tabulate
import copy

class GameNode:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.value = None

    def add_child(self, child):
        self.children.append(child)

    def is_terminal(self):
        return len(self.children) == 0

    def evaluate(self, bot_symbol, opponent_symbol):
        lines = []
        for i in range(5):
            lines.append(self.board[i])
            lines.append([self.board[j][i] for j in range(5)])
        lines.append([self.board[i][i] for i in range(5)])
        lines.append([self.board[i][4 - i] for i in range(5)])

        score = 0
        for line in lines:
            score += self.evaluate_line(line, bot_symbol)
            score -= self.evaluate_line(line, opponent_symbol)
        return score

    @staticmethod
    def evaluate_line(line, symbol):
        count = line.count(symbol)
        empty = line.count(0)
        if count == 5:
            return 1000
        elif count == 4 and empty == 1:
            return 50
        elif count == 3 and empty == 2:
            return 10
        elif count == 2 and empty == 3:
            return 5
        return 0

class GameTree:
    def __init__(self, root):
        self.root = root

    def build_tree(self, bot, depth, maximizing_player):
        self.expand_node(self.root, bot, depth, maximizing_player)

    def expand_node(self, node, bot, depth, maximizing_player):
        if depth == 0 or bot.is_winner(node.board, bot.symbol) or bot.is_winner(node.board, bot.opponent_symbol):
            node.value = node.evaluate(bot.symbol, bot.opponent_symbol)
            return
        moves = bot.generate_moves(node.board, bot.symbol if maximizing_player else bot.opponent_symbol)
        for move in moves:
            new_board = bot.apply_move(node.board, move, bot.symbol if maximizing_player else bot.opponent_symbol)
            child_node = GameNode(new_board, move, node)
            node.add_child(child_node)
            self.expand_node(child_node, bot, depth - 1, not maximizing_player)

class AlphaBeta:
    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        best_state = None

        for child in node.children:
            value = self.min_value(child, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = child
        return best_state

    def max_value(self, node, alpha, beta):
        if node.is_terminal():
            return node.value
        value = float('-inf')
        for child in node.children:
            value = max(value, self.min_value(child, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        if node.is_terminal():
            return node.value
        value = float('inf')
        for child in node.children:
            value = min(value, self.max_value(child, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

class QuixoBot2:
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
        root = GameNode(board)
        tree = GameTree(root)
        tree.build_tree(self, 2, True)
        alphabeta = AlphaBeta()
        best_node = alphabeta.alpha_beta_search(root)
        move = best_node.move if best_node else None
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

    def reset(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 1 if symbol == -1 else -1
        self.board = [[0] * 5 for _ in range(5)]

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
        return all(cell != 0 for row in board for cell in row)

    def generate_moves(self, board, symbol):
        moves = []
        allowed_positions = self.ALLOWED_PIECES_GENERAL
        for direction in ['right', 'left', 'up', 'down']:
            for row, col in allowed_positions:
                if board[row][col] == 0 or board[row][col] == symbol:
                    moves.append((direction, (row, col)))
        return moves

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