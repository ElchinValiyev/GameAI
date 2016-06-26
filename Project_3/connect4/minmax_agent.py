import connect4 as c4
import sys


def get_minmax_move(board, player=1, max_depth=2):
    # Get the result of a minmax run and return the move
    score, move = minmax(board, player, max_depth, 0, player == 1)
    return move


def minmax(board, player, max_depth, current_depth, maximizing):
    # Check if we're done recursing
    if c4.is_board_full(board) or current_depth == max_depth:
        return evaluate(player, board), None

    best_move = None
    if player == 1:
        best_score = -sys.maxint
    else:
        best_score = sys.maxint

    # Go through each move
    for move in range(c4.BOARDWIDTH):
        if not c4.is_valid_move(board, move):  # skipping invalid moves
            continue

        new_board = c4.make_move(board, player, move)

        # Recurse
        current_score, current_move = minmax(new_board, -player, max_depth, current_depth + 1, not maximizing)

        # Update the best score
        if maximizing:  # if player's move, maximize evaluation
            if current_score > best_score:
                best_score = current_score
                best_move = move
        else:  # if opponent's move, minimize evaluation
            if current_score < best_score:
                best_score = current_score
                best_move = move

    # Return the score and the best move
    return best_score, best_move


def evaluate(player, board):
    # Simple heuristic for evaluation
    opp_player = player * -1
    if c4.is_winner(board, player):
        return sys.maxint
    if c4.is_winner(board, player):
        return -sys.maxint

    # Find Streaks for both players
    my_threes = check_open_streak(board, player, 3)
    my_twos = check_open_streak(board, player, 2)
    opp_threes = check_open_streak(board, opp_player, 3)
    opp_twos = check_open_streak(board, opp_player, 2)

    # value to be returned
    value = (my_threes * 1000 + my_twos * 10) - (opp_threes * 1000 + opp_twos * 10)
    return value  # return value and the corresponding column


def check_open_streak(state, color, streak):
    count = 0
    # for each piece in the board...
    for i in xrange(c4.BOARDWIDTH):
        for j in xrange(c4.BOARDHEIGHT):
            # ...that is of the color we're looking for...
            if state[i][j] == color:
                # check if a vertical streak starts at (i, j)
                count += vertical_streak(i, j, state, color, streak)

                # check if a horizontal four-in-a-row starts at (i, j)
                count += horizontal_streak(i, j, state, color, streak)

                # check if a diagonal (either way) four-in-a-row starts at (i, j)
                count += diagonal_check(i, j, state, color, streak)
    # return the sum of streaks of length 'streak'
    return count


def vertical_streak(row, col, state, color, streak):
    # Check for vertical Streaks
    consecutive_count = 0
    for i in range(row, c4.BOARDWIDTH):
        if state[i][col] == color:
            consecutive_count += 1
        else:
            break
    if consecutive_count >= streak:
        return 1
    else:
        return 0


def horizontal_streak(row, col, state, color, streak):
    # Check for horizontal Streaks
    consecutive_count = 0
    for j in range(col, -1, -1):
        if state[row][j] == color:
            consecutive_count += 1
        else:
            break
    if consecutive_count >= streak:
        return 1
    else:
        return 0


def diagonal_check(row, col, state, color, streak):
    # Check both positive and negative diagonals for Streaks
    total = 0

    # check for diagonals with negative slope
    consecutive_count = 0
    j = col
    for i in range(row, c4.BOARDHEIGHT):
        if j > 5:
            break
        elif state[i][j] == color:
            consecutive_count += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutive_count >= streak:
        total += 1

    consecutive_count = 0
    j = col
    for i in range(row, c4.BOARDHEIGHT):
        if j < 0:
            break
        elif state[i][j] == color:
            consecutive_count += 1
        else:
            break
        j -= 1  # increment column when row is incremented
    if consecutive_count >= streak:
        total += 1
    return total


if __name__ == '__main__':
    winners = [0, 0, 0]
    print "Testing"
    for i in xrange(10000):
        winners[c4.play_without_ui(get_minmax_move, c4.get_random_move)] += 1
        print 'Game: ' + str(i)
    c4.plot_results(winners[1], winners[-1], winners[0])
