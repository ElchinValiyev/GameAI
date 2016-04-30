import scipy
from sklearn import preprocessing
import numpy as np

prob_matrix = np.loadtxt("myfile")

countX = 0
countO = 0
countD = 0

def move_still_possible(S):
    return not (S[S==0].size == 0)

def move_with_probability(S, p):

    prob = np.zeros((3,3))

    for i in range(3):
        for j in range(3):
            if(S[i,j]==0):
                prob[i,j] = prob_matrix[i,j]

    x,y = np.where(prob==prob.max())

    S[x[0],y[0]] = p

    return S


def move_at_random(S, p):
    xs, ys = np.where(S==0)

    i = np.random.permutation(np.arange(xs.size))[0]

    S[xs[i],ys[i]] = p


    return S


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False



# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'x', -1:'o', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print B





if __name__ == '__main__':
    for i in np.arange(1000):

        # initialize 3x3 tic tac toe board
        gameState = np.zeros((3,3), dtype=int)

        # initialize player number, move counter
        player = 1
        mvcntr = 1

        # initialize flag that indicates win
        noWinnerYet = True



        while move_still_possible(gameState) and noWinnerYet:
            # get player symbol
            name = symbols[player]
            print '%s moves' % name

            # let player move at random
            if player==-1:
                gameState = move_at_random(gameState, player)
            else:
                gameState = move_with_probability(gameState,player)


            # print current game state
            print_game_state(gameState)

            # evaluate game state
            if move_was_winning_move(gameState, player):
                if(player == 1):
                    countX+=1
                else:
                    countO+=1

                print 'player %s wins after %d moves' % (name, mvcntr)

                noWinnerYet = False

            # switch player and increase move counter
            player *= -1
            mvcntr +=  1






        if noWinnerYet:
            print 'game ended in a draw'
            countD+=1

    print countX
    print countO
    print countD