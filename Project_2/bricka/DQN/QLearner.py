from Environment import Environment
from Memory import Memory
import random
import numpy as np

from keras.layers.core import Dense, Flatten
from keras.layers.convolutional import Convolution2D
from keras.models import Sequential
from keras.models import model_from_json


class Q:
    def __init__(self):
        self.net = None
        self.env = Environment(False, 4)
        self.mem = Memory(32, 1000000)
        self.epsilon = 0.5
        self.gamma = 0.7
        self.number_of_actions = 4
        try:
            self.load_network()
        except IOError:
            print 'No network found'
            self.create_model()

    def create_model(self):
        print 'Creating model...'
        model = Sequential()
        model.add(
            Convolution2D(32, 8, 8, subsample=(4, 4), activation='relu', input_shape=(4, 84, 84)))
        model.add(Convolution2D(64, 4, 4, activation='relu', subsample=(2, 2)))
        model.add(Convolution2D(64, 3, 3, activation='relu', subsample=(1, 1)))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(self.number_of_actions, activation='linear'))
        model.compile(loss='mse', optimizer='rmsprop')
        self.net = model
        print 'Done!'

    def save_network(self):
        json_string = self.net.to_json()
        open('deep_q_network.json', 'w').write(json_string)
        self.net.save_weights('network_weights.h5', overwrite=True)

    def load_network(self):
        print 'Loading network...'
        model = model_from_json(open('deep_q_network.json').read())
        model.load_weights('network_weights.h5')
        model.compile(loss='mse', optimizer='rmsprop')
        print 'Network loaded!'
        self.net = model

    def train(self, epochs):
        for i in xrange(epochs):
            state = self.env.get_state()
            while not self.env.isTerminal():
                qval = self.net.predict(state.reshape(1, 4, 84, 84), batch_size=1)
                if random.random() < self.epsilon:  # choose random action
                    action = np.random.randint(0, self.number_of_actions)
                else:  # choose best action from Q(s,a) values
                    action = np.argmax(qval)
                # Take action, observe new state S'
                reward = self.env.act(action)
                new_state = self.env.get_state()
                # Experience replay storage
                is_terminal = self.env.isTerminal()

                self.mem.store(state, action, reward, new_state, is_terminal)

                print 'Game : {}'.format(i)
                if self.mem.isFull():
                    minibatch = self.mem.sample()
                    self.train_on_minibatch(minibatch)
                state = new_state

            if self.epsilon > 0.1:  # decrement epsilon over time
                self.epsilon -= (1 / 100000)
            self.env.restart()
            if i % 10 == 0:
                self.save_network()

    def train_on_minibatch(self, minibatch):
        x_train, y_train = [], []
        for sample in minibatch:
            # Get max_Q(S',a)
            old_state, action, reward, new_state, terminal = sample
            old_qval = self.net.predict(old_state.reshape(1, 4, 84, 84), batch_size=1)
            newQ = self.net.predict(new_state.reshape(1, 4, 84, 84), batch_size=1)
            maxQ = np.max(newQ)
            y = np.zeros((1, self.number_of_actions))
            y[:] = old_qval[:]
            if not terminal:  # non-terminal state
                update = (reward + (self.gamma * maxQ))
            else:  # terminal state
                update = reward
            y[0][action] = update
            x_train.append(old_state.reshape(4, 84, 84))
            y_train.append(y.reshape(self.number_of_actions, ))

        x_train = np.array(x_train)
        y_train = np.array(y_train)
        self.net.fit(x_train, y_train, batch_size=self.mem.batch_size, nb_epoch=1)

    def play(self):
        environment = Environment(True, 4)
        while not environment.isTerminal():
            state = environment.get_state()
            qval = self.net.predict(state.reshape(1, 4, 84, 84), batch_size=1)
            action = (np.argmax(qval))
            reward = environment.act(action)


if __name__ == "__main__":
    player = Q()
    # player.play()
    player.train(100000)
