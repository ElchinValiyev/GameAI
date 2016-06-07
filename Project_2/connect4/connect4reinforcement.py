"""
Reference implementation of the Tic-Tac-Toe value function learning agent described in Chapter 1 of
"Reinforcement Learning: An Introduction" by Sutton and Barto. The agent contains a lookup table that
maps states to values, where initial values are 1 for a win, 0 for a draw or loss, and 0.5 otherwise.
At every move, the agent chooses either the maximum-value move (greedy) or, with some probability
epsilon, a random move (exploratory); by default epsilon=0.3. The agent updates its value function
(the lookup table) after every greedy move, following the equation:

    V(s) <- V(s) + alpha * [ V(s') - V(s) ]
"""

import random
import Project_2.connect4 as c4
import pickle

EMPTY = 0
PLAYER_X = 1
PLAYER_O = -1
DRAW = 3


def empty_state():
    return c4.getNewBoard()


def game_over(state):
    if c4.isWinner(state, PLAYER_X):
        return PLAYER_X
    if c4.isWinner(state, PLAYER_O):
        return PLAYER_O
    if c4.isBoardFull(state):
        return DRAW
    else:
        return EMPTY


def play(agent1, agent2):
    state = empty_state()
    player = 1
    while not c4.isBoardFull(state):
        if player > 0:
            move = agent1.action(state)
        else:
            move = agent2.action(state)
        state = c4.makeMove(state, player, move)
        winner = game_over(state)
        player *= -1
        if winner != EMPTY:
            return winner
    return winner


class Agent(object):
    def __init__(self, player, lossval=-1):
        self.values = {}
        self.player = player
        self.lossval = lossval
        self.learning = True
        self.epsilon = 0.3
        self.alpha = 0.99
        self.prevstate = None
        self.prevscore = 0
        self.count = 0
        try:
            print "Loading values..."
            with open('values.pickle', 'rb') as handle:
                self.values = pickle.load(handle)
            print "Finished loading!"
        except IOError:
            self.train(100000)

    def episode_over(self, winner):
        self.backup(self.winnerval(winner))
        self.prevstate = None
        self.prevscore = 0

    def action(self, state):
        r = random.random()
        if r < self.epsilon:
            move = self.random(state)
        else:
            move = self.greedy(state)
        new_state = c4.makeMove(state, self.player, move)
        self.prevstate = self.state_string(new_state)
        self.prevscore = self.lookup(new_state)
        return move

    def random(self, state):
        return c4.getRandomMove(state)

    def greedy(self, state):
        maxval = -50000
        maxmove = None
        for i in range(7):
            if c4.isValidMove(state, i):
                new_state = c4.makeMove(state, self.player, i)
                val = self.lookup(new_state)
                if val > maxval:
                    maxval = val
                    maxmove = i
        self.backup(maxval)
        return maxmove

    def backup(self, nextval):
        if self.prevstate is not None and self.learning:
            self.values[self.prevstate] += self.alpha * (nextval - self.prevscore)

    def lookup(self, state):
        key = self.state_string(state)
        if not key in self.values:
            self.add(state)
        return self.values[key]

    def add(self, state):
        winner = game_over(state)
        tup = self.state_string(state)
        self.values[tup] = self.winnerval(winner)

    def winnerval(self, winner):
        if winner == self.player:
            return 1
        elif winner == EMPTY:
            return 0.5
        elif winner == DRAW:
            return 0
        else:
            return self.lossval

    def state_string(self, state):
        return str(state)

    def train(self, times):
        p2 = Agent(2, lossval=-1)
        p2.values = {}
        print "Training started!"
        for i in range(times):
            if i % 1000 == 0:
                print 'Game: {0}'.format(i)
            winner = play(self, p2)
            self.episode_over(winner)
            p2.episode_over(winner)
        with open('values.pickle', 'wb') as handle:
            pickle.dump(self.values, handle)


if __name__ == "__main__":
    p1 = Agent(1, lossval=-1)
    p1.learning = False
    winners = [0, 0, 0]
    for i in range(10000):
        winners[c4.play_without_ui(p1.greedy, c4.getRandomMove)] += 1
    c4.plotResults(winners[1], winners[2], winners[0])
    print winners
