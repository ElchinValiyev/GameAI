from Environment import Environment
from Memory import Memory
import random
import numpy as np

from keras.layers.core import Dense, Flatten
from keras.layers.convolutional import Convolution2D
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.models import model_from_json


class Q:
    def __init__(self):
        self.net = None
        self.epsilon = 1
        self.gamma = 0.975
        self.previous_state = None
        self.number_of_actions = 3
        try:
            self.load_network()
        except IOError:
            print 'No network found'
            self.create_model()

    def create_model(self):
        print 'Creating model...'
        model = Sequential()

        model.add(Convolution2D(32, 8, 8, activation='relu', subsample=(4, 4), input_shape=(1, 84, 84)))
        model.add(Convolution2D(64, 4, 4, activation='relu', subsample=(2, 2)))
        model.add(Convolution2D(64, 3, 3, activation='relu', subsample=(1, 1)))
        model.add(Flatten())
        model.add(Dense(512, init="lecun_uniform", activation='relu'))
        model.add(Dense(self.number_of_actions, init="lecun_uniform", activation='relu'))
        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)
        self.net = model
        print 'Done!'

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

    def train(self, epochs):
        environment = Environment()
        memory = Memory(500, 1000)
        for i in xrange(epochs):
            state = environment.getScreen()
            while not environment.isTerminal():
                qval = self.net.predict(state.reshape(1, 1, 84, 84), batch_size=1)
                if random.random() < self.epsilon:  # choose random action
                    action = np.random.randint(0, self.number_of_actions)
                else:  # choose best action from Q(s,a) values
                    action = (np.argmax(qval))
                # Take action, observe new state S'
                reward = environment.act(action)
                new_state = environment.getScreen()

                # Experience replay storage
                memory.store(state, action, reward, new_state)
                if memory.isFull():
                    minibatch = memory.sample()
                    x_train, y_train = [], []
                    for sample in minibatch:
                        # Get max_Q(S',a)
                        old_state, action, reward, new_state = sample
                        old_qval = self.net.predict(old_state.reshape(1, 1, 84, 84), batch_size=1)
                        newQ = self.net.predict(new_state.reshape(1, 1, 84, 84), batch_size=1)
                        maxQ = np.max(newQ)
                        y = np.zeros((1, self.number_of_actions))
                        y[:] = old_qval[:]
                        if not environment.isTerminal():  # non-terminal state
                            update = (reward + (self.gamma * maxQ))
                        else:  # terminal state
                            update = reward
                        y[0][action] = update
                        x_train.append(old_state.reshape(1, 84, 84))
                        y_train.append(y.reshape(self.number_of_actions, ))

                    x_train = np.array(x_train)
                    y_train = np.array(y_train)
                    print("Game #: %s" % (i,))
                    self.net.fit(x_train, y_train, batch_size=memory.batch_size, nb_epoch=1)
                    state = new_state
            environment.restart()
            if i % 100 == 0:
                self.save_network()


if __name__ == "__main__":
    player = Q()
    player.train(300)
