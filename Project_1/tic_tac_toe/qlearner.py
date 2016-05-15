import numpy as np

import agent
from Board import BoardImplementation as Board


class QLearner:
    def __init__(self):
        self.GAMES = 100000  # number of games for training
        self.ALPHA = 0.2  # learning rate
        self.GAMMA = 0.9  # discount factor
        self.qvalues = {}
        self.last_state = ""
        self.last_action = ""
        try:
            self.__load_qvalues_from_file()
        except IOError:
            self.__train()
            self.__save_qvalues_to_file()

    def __give_feedback(self, current_board, feed_back):
        if current_board.is_over:
            expected = feed_back  # reward from terminal state
        else:  # max reward for current state
            expected = self.__get_max_q(current_board)
        old_state_action = self.last_state + self.last_action
        q_old = self.qvalues.get(old_state_action, 0)
        # updating q-value
        self.qvalues[old_state_action] = q_old + self.ALPHA * (
            feed_back + self.GAMMA * expected - q_old)

    def __get_max_q(self, current_board):
        # find max q value for possible actions
        xs, ys = current_board.get_moves()
        state = str(current_board.state.tolist())
        max_q = self.qvalues.get(state + str(xs[0]) + str(ys[0]), 0)
        for i in range(xs.size):
            next_q = self.qvalues.get(state + str(xs[i]) + str(ys[i]), 0)
            if next_q > max_q:
                max_q = next_q
        return max_q

    def __get_move(self, board):
        # playing randomly for exploration
        return agent.get_random_move(board)

    def __train(self):
        print "Q-learning started!"
        for i in range(self.GAMES):
            if i % 1000 == 0:
                print "Game #" + str(i) + " played!"
            # initialize 3x3 tic tac toe board
            board = Board(3)
            while board.move_still_possible():
                if board.player == 1:  # X-player
                    move = self.__get_move(board)
                    self.last_state = str(board.state.tolist())
                    self.last_action = str(move[0]) + str(move[1])
                    self.__give_feedback(board, 0)
                else:  # O-player
                    move = agent.get_random_move(board)

                board.make_move(move)
                # evaluate game state
                if board.game_is_over():
                    # return winner
                    self.__give_feedback(board, 10 * board.player)
                    break
            self.__give_feedback(board, 5)
        print "Q-learning finished!"

    def get_max_q_move(self, current_board):
        xs, ys = current_board.get_moves()
        x, y = xs[0], ys[0]
        state = str(current_board.state.tolist())
        max_q = self.qvalues.get(state + str(x) + str(y), 0)
        for i in range(xs.size):
            next_q = self.qvalues.get(state + str(xs[i]) + str(ys[i]), 0)
            if next_q > max_q:
                max_q = next_q
                x = xs[i]
                y = ys[i]
        return x, y

    def __save_qvalues_to_file(self):
        # Save
        np.save('qvalues', self.qvalues)

    def __load_qvalues_from_file(self):
        self.qvalues = np.load('qvalues.npy').item()


if __name__ == '__main__':
    q = QLearner()
    print q.qvalues

    board = Board()

    while board.move_still_possible():
        if board.player == 1:  # X-player
            move = q.get_max_q_move(board)
        else:  # O-player
            move = agent.get_minmax_move(board)
        board.make_move(move)
        board.print_game_state()
        # evaluate game state
        if board.game_is_over():
            # return winner
            print board.player
            break
            # return 'game ended in a draw'
