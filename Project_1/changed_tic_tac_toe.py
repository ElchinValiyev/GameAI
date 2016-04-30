import numpy as np
from sklearn import preprocessing
from Board import BoardImplementation as Board
import agent


def one_agent_makes_move(board):
    if board.player == 1:  # X-player
        move = agent.get_random_move(board)
        # move = agent.get_minimax_move(board, 2)
    else: # O-player
        move = agent.get_random_move(board)
        # move = agent.get_minimax_move(board, max_depth=5)
    board.make_move(move)


def play():
    # initialize 3x3 tic tac toe board
    board = Board(3)

    # initialize  move counter
    mvcntr = 1


    while board.move_still_possible():

        # let player move at random
        one_agent_makes_move(board)

        # evaluate game state
        if board.game_is_over():
            return board.player, mvcntr
        mvcntr += 1

    return 0, mvcntr
    # print 'game ended in a draw'

board = Board(3)
agent.learn_probability(board)

