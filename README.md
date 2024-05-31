# Quixo Bot

## Description

QuixoBot is a bot designed to play Quixo, a strategic board game. The bot uses an Alpha-Beta search algorithm to make intelligent decisions during the game. This README provides an overview of the bot's functionality, usage examples, and everything you need to understand and use the code.

## Authors

- [@Kurisari](https://www.github.com/kurisari)

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contents

- [Quixo Bot](#quixo-bot)
  - [Description](#description)
  - [Authors](#authors)
  - [License](#license)
  - [Contents](#contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Initializing the Bot](#initializing-the-bot)
  - [Classes and Methods](#classes-and-methods)
    - [GameNode](#gamenode)
    - [GameTree](#gametree)
    - [AlphaBeta](#alphabeta)
    - [QuixoBot](#quixobot)
  - [Examples](#examples)

## Installation

To use QuixoBot, you need to install the `tabulate` library. You can install it using pip:

```sh
pip install tabulate
```

## Usage

### Initializing the Bot

To initialize the bot and play a game, you need to create an instance of the `QuixoBot` class and use the `play_turn` method to make the bot perform a move. The board is represented as a 5x5 matrix.

```python
from quixo_bot import QuixoBot

# Create a new bot with the symbol 1 (X)
bot = QuixoBot(symbol=1)

# Initial state of the board (empty)
board = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Print the initial board
bot.print_board(board)

# The bot makes a move
new_board = bot.play_turn(board)

# Print the board after the bot's move
bot.print_board(new_board)
```

## Classes and Methods

### GameNode

`GameNode` represents a node in the game tree, containing a board state and the move made to reach that state.

- **Methods:**
  - `__init__(self, board, move=None, parent=None)`: Initializes a game node.
  - `add_child(self, child)`: Adds a child node.
  - `is_terminal(self)`: Checks if the node is terminal (has no children).
  - `evaluate(self, bot_symbol, opponent_symbol)`: Evaluates the node's state.

### GameTree

`GameTree` builds a game tree from a root node.

- **Methods:**
  - `__init__(self, root)`: Initializes the game tree with a root node.
  - `build_tree(self, bot, depth, maximizing_player)`: Builds the game tree to a given depth.
  - `expand_node(self, node, bot, depth, maximizing_player)`: Expands a node in the tree.

### AlphaBeta

`AlphaBeta` implements the Alpha-Beta search algorithm to determine the best move.

- **Methods:**
  - `alpha_beta_search(self, node)`: Performs the Alpha-Beta search from a given node.
  - `max_value(self, node, alpha, beta)`: Calculates the maximum value.
  - `min_value(self, node, alpha, beta)`: Calculates the minimum value.

### QuixoBot

`QuixoBot` is the bot that plays Quixo, using the `GameNode`, `GameTree`, and `AlphaBeta` classes.

- **Methods:**
  - `__init__(self, symbol)`: Initializes the bot with a given symbol.
  - `play_turn(self, board)`: Makes a move on the board.
  - `move_right(self, board, row, col, end_col=4)`: Moves a piece to the right.
  - `move_left(self, board, row, col, end_col=0)`: Moves a piece to the left.
  - `move_up(self, board, row, col, end_row=0)`: Moves a piece up.
  - `move_down(self, board, row, col, end_row=4)`: Moves a piece down.
  - `print_board(self, board=None)`: Prints the board.
  - `reset(self, symbol)`: Resets the bot with a given symbol.
  - `is_winner(self, board, symbol)`: Checks for a winner.
  - `is_full(self, board)`: Checks if the board is full.
  - `generate_moves(self, board, symbol)`: Generates all possible moves.
  - `is_valid_move(self, board, direction, row, col, symbol)`: Checks if a move is valid.
  - `apply_move(self, board, move, symbol)`: Applies a move to the board.

## Examples

Here is an example of how to use QuixoBot in a game:

```python
from quixo_bot import QuixoBot

# Create a new bot with the symbol -1 (O)
bot = QuixoBot(symbol=-1)

# Initial state of the board
board = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Print the initial board
bot.print_board(board)

# The bot makes a move
new_board = bot.play_turn(board)

# Print the board after the bot's move
bot.print_board(new_board)
```
