import random
import connect4 as c4
import numpy as np

from keras.layers.core import Dense, Activation
from keras.models import Sequential
from keras.optimizers import RMSprop
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
        self.epsilon = 0.5
        self.previous_state = None

    def create_model(self):
        print 'Creating model...'
        model = Sequential()
        model.add(Dense(84, init='uniform', input_shape=(126,)))
        model.add(Activation('relu'))
        # model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

        model.add(Dense(42, init='uniform'))
        model.add(Activation('relu'))
        # model.add(Dropout(0.2))

        model.add(Dense(1, init='uniform'))
        model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)
        self.net = model
        print 'Done!'

    def train(self, epochs):
        for i in xrange(epochs):
            if i % 10000 == 0:
                print 'Game: {0}'.format(i)
                # self.save_network()
            winner = self.play()
            self.backup(np.array([winner]))
            self.previous_state = None
        # self.save_network()
        print "Training finished!"

    def play(self):
        state = c4.getNewBoard()
        player = 1
        while not c4.isBoardFull(state):
            if player == 1:
                move = self.action(state, player)
            else:
                move = c4.getRandomMove(state)
            state = c4.makeMove(state, player, move)
            if c4.isWinner(state, player):
                return player
            player *= -1
        return 0.5  # draw

    def action(self, state, player=1):
        if random.random() < self.epsilon:
            move = c4.getRandomMove(state)
        else:
            move = self.greedy(state)
        new_state = c4.makeMove(state, player, move)
        self.previous_state = new_state
        return move

    def greedy(self, state, player=1):
        max_value = float("-inf")
        next_move = None
        # TODO: implemen get_possible_moves in c4
        for move in range(7):
            if c4.isValidMove(state, move):
                new_state = c4.makeMove(state, player, move)
                val = self.net.predict(c4.getNeuralInput(new_state).reshape(1, 126), batch_size=1)
                if val > max_value:
                    max_value = val
                    next_move = move
        self.backup(max_value)
        return next_move

    def backup(self, value):
        if self.previous_state is not None and self.learning:
            self.net.fit(c4.getNeuralInput(self.previous_state).reshape(1, 126), value, batch_size=1,
                         nb_epoch=1)

    def save_network(self):
        json_string = self.net.to_json()
        open('model.json', 'w').write(json_string)
        self.net.save_weights('network_weights.h5', overwrite=True)

    def load_network(self):
        print 'Loading network...'
        model = model_from_json(open('model.json').read())
        model.load_weights('network_weights.h5')
        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)
        print 'Network loaded!'
        self.net = model


if __name__ == "__main__":
    max = 0
    player = TD()
    # player.train(5000)
    winners = [0, 0, 0]
    print "Testing"
    player.learning = False
    for i in xrange(10000):
        winners[c4.play_without_ui(player.greedy, c4.getRandomMove)] += 1
    c4.plotResults(winners[1], winners[-1], winners[0])
