import random
import connect4 as c4
import numpy as np

from keras.layers.core import Dense
from keras.models import Sequential
from keras.models import model_from_json


class TD:
    def __init__(self):
        self.net = None
        self.learning = True
        try:
            self.load_network()
        except IOError:
            print 'Failed to load...'
            self.create_model()
        self.epsilon = 1  # initial exploration rate
        self.previous_state = None

    def create_model(self):
        print 'Creating model...'
        model = Sequential()
        model.add(Dense(19 * 19 * 2, input_shape=(19 * 19 * 3,), activation='relu'))
        model.add(Dense(19 * 19, activation='relu'))
        model.add(Dense(1, activation='linear'))  # linear output so we can have range of real-valued outputs
        model.compile(loss='mse', optimizer='rmsprop')
        self.net = model
        print 'Done!'

    def train(self, epochs):
        for k in xrange(epochs):
            if k % 10000 == 0:
                print 'Game: {0}'.format(k)
                # self.save_network()
            winner = self.play()  # play against opponent
            self.backup(np.array([winner]))  # give reward to the network
            self.previous_state = None
            if self.epsilon > 0.1:  # decrement epsilon over time
                self.epsilon -= (1 / epochs)
        self.save_network()
        print "Training finished!"

    def play(self):
        state = c4.get_new_board()
        player = 1
        while not c4.is_board_full(state):
            if player == 1:  # TD player plays as first player
                move = self.action(state, player)
            else:
                move = c4.get_random_move(state)  # random player is second
            state = c4.make_move(state, player, move)
            if c4.is_winner(state, player):
                return player
            player *= -1
        return 0.5  # draw

    def action(self, state, player=1):  # by default TD plays as first player
        if random.random() < self.epsilon:
            move = c4.get_random_move(state)  # exploration move
        else:
            move = self.greedy(state)  # exploitation move
        new_state = c4.make_move(state, player, move)
        self.previous_state = new_state
        return move

    def greedy(self, state, player=1):
        max_value = float("-inf")
        next_move = None
        for move in range(c4.BOARDWIDTH):
            if c4.is_valid_move(state, move):  # checking only valid moves
                new_state = c4.make_move(state, player, move)
                # estimate of new state
                val = self.net.predict(c4.get_neural_input(new_state).reshape(1, 1083), batch_size=1)
                if val > max_value:  # searching move with best estimate
                    max_value = val
                    next_move = move
        self.backup(max_value)
        return next_move

    def backup(self, value):  # updating TD values
        if self.previous_state is not None and self.learning:
            self.net.fit(c4.get_neural_input(self.previous_state).reshape(1, 1083), value, batch_size=1,
                         nb_epoch=1)

    def save_network(self):
        json_string = self.net.to_json()  # transform network in JSON
        open('model.json', 'w').write(json_string)  # saving network structure
        self.net.save_weights('network_weights.h5', overwrite=True)  # saving network weights

    def load_network(self):
        print 'Loading network...'
        model = model_from_json(open('model.json').read())  # load model from file
        model.load_weights('network_weights.h5')  # load network weights
        model.compile(loss='mse', optimizer='rmsprop')
        print 'Network loaded!'
        self.net = model


if __name__ == "__main__":
    player = TD()
    player.train(300000)
    winners = [0, 0, 0]
    print "Testing"
    player.learning = False
    for i in xrange(10000):
        winners[c4.play_without_ui(player.greedy, c4.get_random_move)] += 1
    c4.plot_results(winners[1], winners[-1], winners[0])
