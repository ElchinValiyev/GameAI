import connect4 as c4


def get_negamax_move(board, player=1, max_depth=2):
    """Get the result of a ab-negamax run and return the move"""
    score, move = alpha_beta_negamax(board, player, max_depth, 0, float('-inf'), float('inf'))
    return move


def alpha_beta_negamax(board, player, max_depth, current_depth, alpha, beta):
    # Check if we're done recursing
    if c4.is_board_full(board) or current_depth == max_depth:
        return evaluate(player, board), None

    best_move = None
    best_score = float('-inf')
    # Go through each move
    for move in range(c4.BOARD_WIDTH):
        if not c4.is_valid_move(board, move):  # skipping invalid moves
            continue

        new_board = c4.make_move(board, player, move)
        # Recurse
        recursed_score, current_move = alpha_beta_negamax(new_board, -player, max_depth, current_depth + 1,
                                                          -beta, -max(alpha, best_score))
        current_score = -recursed_score

        # Update the best score
        if current_score >= best_score:
            best_score = current_score
            best_move = move
            if best_score >= beta:  # If we're outside the bounds, then prune: exit immediately
                return best_score, best_move
    # Return the score and the best move
    return best_score, best_move


def evaluate(player, board):
    """Simple heuristic for evaluation"""
    opp_player = player * -1
    if c4.is_winner(board, player):
        return float('inf')
    if c4.is_winner(board, opp_player):
        return float('-inf')

    # Find Streaks for both players
    my_threes = check_open_streak(board, player, 3)
    my_twos = check_open_streak(board, player, 2)
    opp_threes = check_open_streak(board, opp_player, 3)
    opp_twos = check_open_streak(board, opp_player, 2)

    # value to be returned
    value = (my_threes * 1000 + my_twos * 100) - (opp_threes * 1000 + opp_twos * 100)
    return value  # return value and the corresponding column


def check_open_streak(board, player, streak):
    count = 0
    # for each piece in the board...
    for i in xrange(c4.BOARD_WIDTH):
        for j in xrange(c4.BOARD_HEIGHT):
            # ...that is of the color we're looking for...
            if board[i][j] == player:
                # check if a vertical streak starts at (i, j)
                count += vertical_streak(i, j, board, player, streak)

                # check if a horizontal four-in-a-row starts at (i, j)
                count += horizontal_streak(i, j, board, player, streak)

                # check if a diagonal (either way) four-in-a-row starts at (i, j)
                count += diagonal_check(i, j, board, player, streak)
    # return the sum of streaks of length 'streak'
    return count


def horizontal_streak(row, col, board, player, streak):
    """Check for vertical Streaks"""
    consecutive_count = 0
    for i in range(row, c4.BOARD_WIDTH):  # looking to the left
        if board[i][col] == player:
            consecutive_count += 1
        else:
            break
    if consecutive_count >= streak:
        return 1
    else:
        return 0


def vertical_streak(row, col, board, player, streak):
    """Checks for horizontal Streaks"""
    consecutive_count = 0
    for j in range(col, c4.BOARD_HEIGHT):
        if board[row][j] == player:
            consecutive_count += 1
        else:
            break
    if consecutive_count >= streak:
        return 1
    else:
        return 0


def diagonal_check(row, col, board, player, streak):
    """Checks both positive and negative diagonals for Streaks"""
    total = 0

    # check for diagonals with negative slope
    consecutive_count = 0
    j = col
    for i in range(row, c4.BOARD_WIDTH):
        if j > c4.BOARD_HEIGHT - 1:
            break
        elif board[i][j] == player:
            consecutive_count += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutive_count >= streak:
        total += 1

    consecutive_count = 0
    j = col
    for i in range(row, c4.BOARD_WIDTH):
        if j < 0:
            break
        elif board[i][j] == player:
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
        winners[c4.play_without_ui(get_negamax_move, c4.get_random_move)] += 1
        print 'Game: ' + str(i)
    c4.plot_results(winners[1], winners[-1], winners[0], 'AB Negamax vs Random')
>>>>>>> adb0cba5c24b9ac69c1cdb13c465cb55ccf38968:Project_3/connect4/ab_negamax_agent.py
