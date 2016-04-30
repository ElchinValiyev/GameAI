import numpy as np
import sys


class BoardImplementation:
    def __init__(self, size):
        self.is_over = False
        self.player = 1
        self.board = np.zeros((size, size), dtype=int)
        self.coefficients = [3, 1, -3, -1]

    def get_moves(self):
        """ :return  x and y positions of empty cells """
        return np.where(self.board == 0)

    def evaluate(self, player):
        """"
        Static evaluation function

        Eval = 3*X2 + X1 - (3*O2 + O1)
        X2 = number of lines with 2 X's and a blank
        X1 = number of lines with 1 X and 2 blanks
        O2 = number of lines with 2 O's and a blank
        O1 = number of lines with 1 O and 2 blanks
        Return Infinity if X wins and -Infinity if O wins

        Russell & Norvig
        Games, evaluation functions
        :return
            one value, positive for advantage to one player, negative
            means advantage to the other. Zero indicates it is even.
        """
        values = [0, 0, 0, 0]  # [x2,x1,o2,o1]
        winner = [0]  # MaxInt  if player wins or MinInt if opponent

        def check(prod_array, sum_array):
            """ Updates elements of values list"""
            for i in range(0, prod_array.size):
                if prod_array[i] == 0:
                    if sum_array[i] == 2 * player:
                        values[0] += 1
                    elif sum_array[i] == player:
                        values[1] += 1
                    elif sum_array[i] == -2 * player:
                        values[2] += 1
                    elif sum_array[i] == -player:
                        values[3] += 1
                else:  # no empty place in the line
                    self.is_over = True
                    if sum_array[i] == 3 * player:
                        winner[0] = sys.maxint
                    elif sum_array[i] == -3 * player:
                        winner[0] = -sys.maxint - 1

        # checking rows and columns
        for ax in range(0, 2):
            prods = np.product(self.board, axis=ax)
            sums = np.sum(self.board, axis=ax)
            check(prods, sums)

        # checking main diagonal
        main_diag = np.diag(self.board)
        check(np.array([main_diag.prod()]), np.array([main_diag.sum()]))

        # checking other diagonal
        nonmain_diag = np.diag(np.rot90(self.board))
        check(np.array([nonmain_diag.prod()]), np.array([nonmain_diag.sum()]))

        return winner[0] if winner[0] != 0 else np.sum(np.multiply(values, self.coefficients))

    def move_still_possible(self):
        """"Checks if there is an empty cell on the board"""
        self.is_over = (self.board[self.board == 0].size == 0)
        return not self.is_over

    def make_move(self, (x, y)):
        self.board[x, y] = self.player
        self.move_was_winning_move(self.player)


        if not self.is_over:
            self.player *= -1
        return self

    # relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
    symbols = {1: 'x', -1: 'o', 0: ' '}

    # print game state matrix using symbols
    def print_game_state(self):
        b = np.copy(self.board).astype(object)
        for n in [-1, 0, 1]:
            b[b == n] = self.symbols[n]
        print b

    def move_was_winning_move(self, player):
        if np.max((np.sum(self.board, axis=0)) * player) == 3:
            self.is_over = True
        elif np.max((np.sum(self.board, axis=1)) * player) == 3:
            self.is_over = True
        elif (np.sum(np.diag(self.board)) * player) == 3:
            self.is_over = True
        elif (np.sum(np.diag(np.rot90(self.board))) * player) == 3:
            self.is_over = True
        else:
            self.is_over = False
        return self.is_over

    def copy(self):
        new_board = BoardImplementation(0)
        new_board.board = self.board.copy()
        new_board.player = self.player
        new_board.is_over = self.is_over
        return new_board

    def current_player(self):
        return self.player

    def game_is_over(self):
        return self.is_over
