import random
from collections import deque


class Memory:
    def __init__(self, batch_size, buffer_size=10000):
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.buffer = deque(maxlen=buffer_size)

    def store(self, state, action, reward, new_state, terminal):
        self.buffer.append((state, action, reward, new_state, terminal))

    def sample(self):
        # randomly sample our experience replay memory
        return random.sample(self.buffer, self.batch_size)

    def isFull(self):
        return len(self.buffer) == self.buffer_size
