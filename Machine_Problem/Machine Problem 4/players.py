# +-----------------------------------------------------------------------------+
# | Araullo, John Art Marie G.                                                  |
# | BSCS-NS-3A                                                                  |
# | CS321L-M - Artificial Intelligence                                          |
# | Machine Problem #4                                                          |
# | Six Men's Morris Game: The game can be played User vs. AI or User vs. User. |
# | Algorithm: Minimax with Alpha-Beta Pruning; Cutting Off Search              |
# | Please run the program on vscode terminal or pycharm.                       |
# +-----------------------------------------------------------------------------+

from board import Board
import random

# Color functions for printing colored text in the console
color_mode = True # Set to False to disable colors
if color_mode:
    def g(s): return '\033[92m' + s + '\033[0m'
    def b(s): return '\033[94m' + s + '\033[0m'
else:
    def g(s): return s
    def b(s): return s

# Utility functions for converting between positions and symbols
def pos_to_sym(i):
    return chr(ord('a')+i)

def sym_to_pos(i):
    return ord(i) - ord('a')

# Player class representing player in the game
class Player:
    def __init__(self, id, board):
        self.id = id
        self.symbol = '#' if id == 1 else '@'  # Player 1: # Player 2: @
        self.board = board # Reference to the game board

    def get_id(self):
        return self.id

    def get_symbol(self):
        return self.symbol

# AI class representing AI player
class AI(Player):
    def __init__(self, id, board, opponent):
        super().__init__(id, board)
        self.depth_range = (3, 6)  # Depth range for the minimax algorithm
        self.opponent_player = opponent

    # Minimax algorithm with alpha-beta pruning
    def cutoff_search(self, board, depth, maximizing_player, alpha=-float('inf'), beta=float('inf')):
        player = self if maximizing_player else self.opponent_player
        if depth == 0 or board.check_win(player, self.opponent_player):
            return self.evaluate(board)

        if maximizing_player:
            value = -float('inf')
            for i in range(len(board.state)):
                if board.state[i] == self.get_symbol():
                    for j, k in board.edges:
                        if board.check_move(i, j, self):
                            board.move_piece(i, j, self)
                            value = max(value, self.cutoff_search(board, depth - 1, False, alpha, beta))
                            board.move_piece(j, i, self)
                            alpha = max(alpha, value)
                            if alpha >= beta:
                                break
                        if board.check_move(i, k, self):
                            board.move_piece(i, k, self)
                            value = max(value, self.cutoff_search(board, depth - 1, False, alpha, beta))
                            board.move_piece(k, i, self)
                            alpha = max(alpha, value)
                            if alpha >= beta:
                                break
                    if alpha >= beta:
                        break
            return value
        else:
            value = float('inf')
            for i in range(len(board.state)):
                if board.state[i] == player.get_symbol():
                    for j, k in board.edges:
                        if board.check_move(i, j, player):
                            board.move_piece(i, j, player)
                            value = min(value, self.cutoff_search(board, depth - 1, True, alpha, beta))
                            board.move_piece(j, i, player)
                            beta = min(beta, value)
                            if beta <= alpha:
                                break
                        if board.check_move(i, k, player):
                            board.move_piece(i, k, player)
                            value = min(value, self.cutoff_search(board, depth - 1, True, alpha, beta))
                            board.move_piece(k, i, player)
                            beta = min(beta, value)
                            if beta <= alpha:
                                break
                    if beta <= alpha:
                        break
            return value

    # Evaluate the current board state
    def evaluate(self, board):
        # Calculate player and opponent pieces
        player_pieces = 0
        opponent_pieces = 0
        for i in range(len(board.state)):
            if board.state[i] == self.get_symbol():
                player_pieces += 1
            elif board.state[i] == self.opponent_player.get_symbol():
                opponent_pieces += 1

        # Calculate player and opponent mills
        player_mills = sum([1 for mill in board.mills if all(board.state[pos] == self.get_symbol() for pos in mill)])
        opponent_mills = sum([1 for mill in board.mills if all(board.state[pos] == self.opponent_player.get_symbol() for pos in mill)])

        # Calculate player and opponent potential mills
        player_potential_mills = sum([1 for mill in board.mills if any(board.state[pos] == '.' for pos in mill) and all(board.state[pos] == self.get_symbol() or board.state[pos] == '.' for pos in mill)])
        opponent_potential_mills = sum([1 for mill in board.mills if any(board.state[pos] == '.' for pos in mill) and all(board.state[pos] == self.opponent_player.get_symbol() or board.state[pos] == '.' for pos in mill)])

        # Calculate player and opponent scores based on pieces, mills, and potential mills
        player_score = player_pieces * 10 + player_mills * 50 + player_potential_mills * 20
        opponent_score = opponent_pieces * 10 + opponent_mills * 50 + opponent_potential_mills * 20

        return player_score - opponent_score

    # Choose a position to put the piece
    def next_put(self):
        empty_positions = [i for i, val in enumerate(self.board.state) if val == '.']
        x = random.choice(empty_positions)  # Choose from empty positions
        self.board.put_piece(x, self)
        return x

    # Choose what piece to move (move a piece from one position to another)
    def next_move(self):
        depth = random.randint(*self.depth_range)
        best_move = None
        best_value = -float('inf')
        for i in range(len(self.board.state)):
            if self.board.state[i] == self.get_symbol():
                for j, k in self.board.edges:
                    if self.board.check_move(i, j, self):
                        self.board.move_piece(i, j, self)
                        value = self.cutoff_search(self.board, depth - 1, False)
                        self.board.move_piece(j, i, self)
                        if value > best_value:
                            best_value = value
                            best_move = (i, j)
                    if self.board.check_move(i, k, self):
                        self.board.move_piece(i, k, self)
                        value = self.cutoff_search(self.board, depth - 1, False)
                        self.board.move_piece(k, i, self)
                        if value > best_value:
                            best_value = value
                            best_move = (i, k)
        if best_move:
            self.board.move_piece(best_move[0], best_move[1], self)
        return best_move

    # Choose opponent's piece to remove
    def next_remove(self, opponent):
        opponent_positions = [i for i in range(len(self.board.state)) if self.board.state[i] == opponent.get_symbol()]
        x = random.choice(opponent_positions) if opponent_positions else None
        if x is not None:
            self.board.remove_piece(x, opponent)
        return x
    
# Human class representing human player
class Human(Player):
    def __init__(self, id, board):
        super().__init__(id, board)

    # Choose a position to put the piece
    def next_put(self):
        valid_flag = True
        while valid_flag:
            x = input('{} [Put] (pos): '.format(g('Player 1') if self.id == 1 else b('Player 2'))).lower().strip()
            if len(x) != 1 or not x.islower() or not x.isalpha():
                print('Invalid Put-Movement. Please enter a lowercase letter.')
            else:
                x = sym_to_pos(x)
                if not self.board.check_put(x):
                    print('Invalid Put-Movement. Position already occupied or out of range.')
                else:
                    valid_flag = False
        self.board.put_piece(x, self)
        return x

    # Choose what piece to move (move a piece from one position to another)
    def next_move(self):
        valid_flag = True
        while valid_flag:
            x = input('{} [Move] (from to): '.format(g('Player 1') if self.id == 1 else b('Player 2'))).lower().strip().split(' ')
            if len(x) != 2:
                print('Invalid Move. Please enter two lowercase letters separated by a space.')
            else:
                xs, xt = x
                if len(xs) != 1 or len(xt) != 1 or not xs.isalpha() or not xt.isalpha():
                    print('Invalid Move. Please enter two lowercase letters separated by a space.')
                else:
                    xs = sym_to_pos(xs)
                    xt = sym_to_pos(xt)
                    if not self.board.check_move(xs, xt, self):
                        print('Invalid Move. The move is not allowed.')
                    else:
                        valid_flag = False
        self.board.move_piece(xs, xt, self)
        return xt

    # Choose opponent's piece to remove
    def next_remove(self, opponent):
        valid_flag = True
        while valid_flag:
            x = input('{} [Remove] (pos): '.format(g('Player 1') if self.id == 1 else b('Player 2'))).lower().strip()
            if len(x) != 1:
                print('Invalid Put-Movement.')
            else:
                x = sym_to_pos(x)
                if not self.board.check_remove(x, opponent):
                    print('Invalid Put-Movement.')
                else:
                    valid_flag = False
        self.board.remove_piece(x, opponent)