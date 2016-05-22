import numpy as np
import sys

from sklearn import preprocessing

from Board import BoardImplementation as Board


def get_random_move(board):
    xs, ys = board.get_moves()
    i = np.random.randint(0, xs.size)
    return xs[i], ys[i]


def get_minmax_move(board, max_depth=2):
    # Get the result of a minimax run and return the move
    score, move = minmax(board, board.player, max_depth, 0)
    return move


def minmax(board, player, max_depth, current_depth):
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
    for i in range(moves_x.size):
        new_board = board.copy()
        new_board.make_move((moves_x[i], moves_y[i]))

        # Recurse
        current_score, current_move = minmax(new_board, player, max_depth, current_depth + 1)

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


def learn_probabilities():

    # Global counters for winning moves of X and O
    winX = np.zeros((3, 3))
    winO = np.zeros((3, 3))

    # Learn through 50000 plays
    for i in range(5000):
        board = Board(3)

        # Local counters
        countX = np.zeros((3, 3))
        countO = np.zeros((3, 3))
        while board.move_still_possible():
            move = get_random_move(board)
            x, y = move

            # Update corresponding local counter
            if board.player == 1:
                countX[x, y] += 1
            else:
                countO[x, y] += 1
            board.make_move(move)

            if board.move_was_winning_move(board.player):
                winner = board.player

                # Update winner's global counter
                if winner == 1:
                    winX += countX
                elif winner == -1:
                    winO += countO
                break

    # Collect statistics of winning moves of both players
    win = winX + winO

    # Normalize to obtain probabilities
    win_normalized = preprocessing.normalize(win, norm='l2')

    # Write probabilities to file
    f = open('probabilities', 'w')
    np.savetxt(f, win_normalized)
    print "Learning finished!"
    return win_normalized


def get_probabilistic_move(board):
    try:
        # Obtain probabilities from file
        prob_matrix = np.loadtxt("probabilities")
    except IOError:

        # Learn, if there is no file with probabilities
        prob_matrix = learn_probabilities()

    prob = np.zeros((3, 3))

    # Choose valid move which has highest probability
    for i in range(3):
        for j in range(3):
            if board.state[i, j] == 0:
                prob[i, j] = prob_matrix[i, j]
    x, y = np.where(prob == prob.max())
    return x[0], y[0]
