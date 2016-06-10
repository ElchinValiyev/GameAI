import random
import numpy as np

from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.models import model_from_json


class Q:
    def __init__(self):
        self.net = None
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

        model.add(Convolution2D(32, 8, 8, border_mode='same', input_shape=(1, 210, 160), activation='relu'))
        model.add(Convolution2D(64, 4, 4, border_mode='same', activation='relu'))
        model.add(Convolution2D(64, 3, 3, border_mode='same', activation='relu'))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dense(3, activation='linear'))

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


if __name__ == "__main__":
    player = Q()
