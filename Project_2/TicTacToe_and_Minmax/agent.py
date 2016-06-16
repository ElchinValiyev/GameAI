import sys


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
