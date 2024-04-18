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
from players import Human, AI

class SixMensMorris:
    def __init__(self):
        self.board = Board()
        self.players = [] 
        self.num_play = 0

    def next_player(self):
        self.num_play += 1 # Increment the play count
        return self.players[1 - self.num_play % 2] # Alternate between players based on the play count

    def opponent(self, player):
        # Return the opponent of the given player based on the play count
        return self.players[self.num_play % 2]

    def check_win(self, player):
        if_win = False # Flag to track if the player has won
        # Check if the player has won by calling the board's check_win method
        if self.board.check_win(player, self.opponent(player)):
            print('Congratulation to the winner: {}!'.format(self.g('Player 1') if player.get_id() == 1 else self.b('Player 2')))
            if_win = True # Set the flag to True if the player has won
        return if_win # Return the flag indicating if the player has won


    def start_game(self):
        def g(s): return '\033[92m' + s + '\033[0m'
        def b(s): return '\033[94m' + s + '\033[0m'

        print('Please choose Player 1:')
        print('1. Human Player')
        print('2. Computer Player')
        x = input('Your choice is: ')
        if x == '1':
            # Add a Human player with ID 1 to the game
            self.players.append(Human(1, self.board))
            print('Player 1 is a human.')
        elif x == '2':
            # Add an AI player with ID 1 to the game, using Human as the opponent
            opponent_player = Human(2, self.board)  # Human player as the opponent for AI
            self.players.append(AI(1, self.board, opponent_player))
            print('Player 1 is a computer.')

        print('Please choose Player 2:')
        print('1. Human Player')
        print('2. Computer Player')
        x = input('Your choice is: ')
        if x == '1':
            # Add a Human player with ID 2 to the game
            self.players.append(Human(2, self.board))
            print('Player 2 is a human.')
        elif x == '2':
            # Add an AI player with ID 2 to the game, using Human as the opponent
            opponent_player = Human(1, self.board)  # Human player as the opponent for AI
            self.players.append(AI(2, self.board, opponent_player))
            print('Player 2 is a computer.')

        self.board.print_board()
        end = False # Flag to track game end
        while not end:
            player = self.next_player() # Get the next player to make a move
            if self.num_play <= 12:
                x = player.next_put() # Call next_put for putting a piece
            else:
                x = player.next_move() # Call next_move for moving a piece
            self.board.print_board() # Update game board

            if self.num_play > 12 and self.check_win(player):
                end = True # End the game if a player wins
            else:
                if self.board.form_mill(x, player):
                    print('You form a mill!') # A mill is formed
                    player.next_remove(self.opponent(player)) # Call next_remove for removing opponent's piece
                    self.board.print_board() # Update game board

                if self.num_play > 12 and self.check_win(player):
                    end = True

    def g(self, s): return '\033[92m' + s + '\033[0m'
    def b(self, s): return '\033[94m' + s + '\033[0m'

if __name__ == "__main__":
    game = SixMensMorris()
    game.start_game()
