import numpy as np
import sys
from sklearn import preprocessing
from Board import BoardImplementation as Board

def get_random_move(board):
    xs, ys = board.get_moves()
    i = np.random.randint(0, xs.size)
    return xs[i], ys[i]


def get_minimax_move(board, max_depth=2):
    # Get the result of a minimax run and return the move
    score, move = minimax(board, board.player, max_depth, 0)
    return move


def minimax(board, player, max_depth, current_depth):
    # Check if we're done recursing
    if board.game_is_over() or current_depth == max_depth:
        return board.evaluate(player), (None, None)

    best_move = (None, None)
    if board.current_player() == player:
        best_score = -sys.maxint + 1
    else:
        best_score = sys.maxint
    moves_x, moves_y = board.get_moves()

    # Go through each move
    for i in range(0, moves_x.size):
        new_board = board.copy()
        new_board.make_move((moves_x[i], moves_y[i]))

        # Recurse
        current_score, current_move = minimax(new_board, player, max_depth, current_depth + 1)

        # Update the best score
        if board.current_player() == player:
            if current_score > best_score:
                best_score = current_score
                best_move = (moves_x[i], moves_y[i])
        else:
            if current_score < best_score:
                best_score = current_score
                best_move = (moves_x[i], moves_y[i])

    # Return the score and the best move
    return best_score, best_move


def learn_probability(board):
    winX = np.zeros((3, 3))
    winO = np.zeros((3, 3))
    for i in range(1000):
        board = Board(3)
        countX = np.zeros((3, 3))
        countO = np.zeros((3, 3))
        while board.move_still_possible():
            move = get_random_move(board)
            x, y = move

            if (board.player == 1):
                countX[x,y] += 1
            else:
                countO[x,y] += 1
            board.make_move(move)

            winner = 0
            if(board.move_was_winning_move(board.player)):
                winner = board.player
                if winner == 1:
                    winX += countX
                elif winner == -1:
                    winO += countO
                break

    win = winX + winO
    win_normalized = preprocessing.normalize(win, norm='l2')
    f = open('probabilities', 'w')
    np.savetxt(f, win_normalized)

