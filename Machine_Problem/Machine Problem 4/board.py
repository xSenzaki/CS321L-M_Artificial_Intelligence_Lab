# +-----------------------------------------------------------------------------+
# | Araullo, John Art Marie G.                                                  |
# | BSCS-NS-3A                                                                  |
# | CS321L-M - Artificial Intelligence                                          |
# | Machine Problem #4                                                          |
# | Six Men's Morris Game: The game can be played User vs. AI or User vs. User. |
# | Algorithm: Minimax with Alpha-Beta Pruning; Cutting Off Search              |
# | Please run the program on vscode terminal or pycharm.                       |
# +-----------------------------------------------------------------------------+

import random

class Board:
    def __init__(self):
        # Initialize the board state with 16 positions, all empty initially
        self.state = ['.' for _ in range(16)]
        # Define mill configurations and edges for checking moves and mills
        self.mills = [[0, 1, 2], [3, 4, 5], [10, 11, 12], [13, 14, 15],
                      [0, 6, 13], [3, 7, 10], [5, 8, 12], [2, 9, 15]]
        self.edges = [[0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [8, 9], [10, 11], [11, 12],
                      [13, 14], [14, 15], [0, 6], [6, 13], [3, 7], [7, 10], [1, 4], [11, 14],
                      [5, 8], [8, 12], [2, 9], [9, 15]]

    def print_board(self):
        def color(x):
            if x == '.':
                return x
            return g(x) if x == '#' else b(x)

        def g(s): return '\033[92m' + s + '\033[0m'
        def b(s): return '\033[94m' + s + '\033[0m'

        # Visualization
        # Print the board layout with positions and separators
        print(color(self.state[0]), '-' * 9, color(self.state[1]), '-' * 9, color(self.state[2]), end='    ')
        print('a', '-' * 9, 'b', '-' * 9, 'c')
        # Print row separators and positions
        print('|   ', ' ' * 6, '|', ' ' * 6, '   |', end='    ')
        print('|   ', ' ' * 6, '|', ' ' * 6, '   |')
        # Print middle row with pieces and separators
        print('|   ', color(self.state[3]), '-' * 4, color(self.state[4]), '-' * 4, color(self.state[5]), '   |', end='    ')
        print('|   ', 'd', '-' * 4, 'e', '-' * 4, 'f', '   |')
        # Print middle row separators
        print('|   ' * 2, ' ' * 7, '   |' * 2, end='    ')
        print('|   ' * 2, ' ' * 7, '   |' * 2)
        # Print bottom row with pieces and separators
        print(color(self.state[6]), '-', color(self.state[7]), ' ' * 13, color(self.state[8]), '-', color(self.state[9]), end='    ')
        print('g', '-', 'h', ' ' * 13, 'i', '-', 'j')
        # Print bottom row separators
        print('|   ' * 2, ' ' * 7, '   |' * 2, end='    ')
        print('|   ' * 2, ' ' * 7, '   |' * 2)
        # Print last row with pieces and separators
        print('|   ', color(self.state[10]), '-' * 4, color(self.state[11]), '-' * 4, color(self.state[12]), '   |', end='    ')
        print('|   ', 'k', '-' * 4, 'l', '-' * 4, 'm', '   |')
        # Print last row separators and positions
        print('|   ', ' ' * 6, '|', ' ' * 6, '   |', end='    ')
        print('|   ', ' ' * 6, '|', ' ' * 6, '   |')
        # Print final row with pieces and separators
        print(color(self.state[13]), '-' * 9, color(self.state[14]), '-' * 9, color(self.state[15]), end='    ')
        print('n', '-' * 9, 'o', '-' * 9, 'p')

    def check_put(self, pos):
        # Check if a piece can be put at a given position
        if pos < 0 or pos > 15:
            return False
        if self.state[pos] == '#' or self.state[pos] == '@':
            return False
        return True

    def check_move(self, s, t, player):
        # Check if a move from position 's' to position 't' is valid for the player
        if s < 0 or s > 15 or t < 0 or t > 15:
            return False
        if self.state[s] != player.get_symbol() or self.state[t] != '.':
            return False
        for j, k in self.edges:
            if (s == j and t == k) or (s == k and t == j):
                return True
        return False

    def check_remove(self, pos, player):
        # Check if a piece can be removed from a given position by the player
        if pos < 0 or pos > 15:
            return False
        if self.state[pos] != player.get_symbol():
            return False
        return True

    def put_piece(self, pos, player):
        # Put a player's piece at a given position
        self.state[pos] = player.get_symbol()

    def move_piece(self, s, t, player):
        # Move a player's piece from position 's' to position 't'
        if self.check_move(s, t, player):
            self.state[s] = '.'
            self.state[t] = player.get_symbol()

    def remove_piece(self, pos, player):
        # Remove a player's piece from a given position
        if self.check_remove(pos, player):
            self.state[pos] = '.'

    def form_mill(self, pos, player):
        # Check if a player has formed a mill after placing a piece at position 'pos'
        mill_pos = []
        symbol = player.get_symbol()
        for mill_list in self.mills:
            if pos in mill_list:
                mill_pos.append(mill_list)

        for position in mill_pos:
            if self.state[position[0]] == symbol and self.state[position[1]] == symbol and self.state[position[2]] == symbol:
                return True

        return False

    def check_win(self, player, opponent):
        # Check if a player has won the game
        num_pieces = 0
        for i in range(len(self.state)):
            if self.state[i] == opponent.get_symbol():
                num_pieces += 1

        if num_pieces <= 2:
            return True

        can_move = False
        for i in range(len(self.state)):
            if self.state[i] == opponent.get_symbol():
                piece_can_move = False
                for j, k in self.edges:
                    if (i == j and self.check_put(k)) or (i == k and self.check_put(j)):
                        piece_can_move = True
                        break
                if piece_can_move:
                    can_move = True
                    break
        if not can_move:
            return True

        return False
