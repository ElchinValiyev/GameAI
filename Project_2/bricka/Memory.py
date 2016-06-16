import random


class Memory:
    def __init__(self, batch_size, buffer_size=100000):
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.buffer = []
        self.oldest = 0

    def store(self, state, action, reward, new_state):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append((state, action, reward, new_state))
        else:  # if buffer full, overwrite old values
            self.oldest = (self.oldest + 1) % self.buffer_size
            self.buffer[self.oldest] = (state, action, reward, new_state)

    def sample(self):
        # randomly sample our experience replay memory
        return random.sample(self.buffer, self.batch_size)

    def isFull(self):
        return len(self.buffer) == self.buffer_size
