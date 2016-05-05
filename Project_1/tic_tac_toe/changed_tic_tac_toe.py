from Board import BoardImplementation as Board


def play(agent_1, agent_2):
    # initialize 3x3 tic tac toe board
    board = Board(3)
    while board.move_still_possible():

        if board.player == 1:  # X-player
            move = agent_1(board)
        else:  # O-player
            move = agent_2(board)
        board.make_move(move)
        # evaluate game state
        if board.game_is_over():
            # return winner
            return board.player
    # return 'game ended in a draw'
    return 0
