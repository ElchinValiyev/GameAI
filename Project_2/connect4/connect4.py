import matplotlib.pyplot as plt
import numpy as np
import random

BOARDWIDTH = 7
BOARDHEIGHT = 6
EMPTY = 0


def make_autopct(values):
    def my_autopct(pct):
        if pct == 0:
            return ""
        else:
            return '{p:.2f}% '.format(p=pct)
    return my_autopct


def plotResults(red_wins, black_wins, tie):
    # Setting up plot variables
    labels = ['Red Wins', 'Black Wins', 'Ties']
    sizes = [red_wins, black_wins, tie]
    colors = ['yellowgreen', 'gold', 'lightskyblue']
    explode = (0.1, 0, 0)

    plt.pie(sizes, colors=colors, autopct=make_autopct(sizes), explode=explode, labels=labels, shadow=True,
            startangle=70)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
    print "number of red wins ", red_wins
    print "number of black wins ", black_wins
    print "number of ties ", tie


def makeMove(board, player, column):
    new_board = board.copy()
    # Finding the lowest row for the selected column to place the player
    lowest = getLowestEmptySpace(new_board, column)
    if lowest != -1:
        new_board[column][lowest] = player
    return new_board


def getNewBoard():
    # Create a new board and initilize all fields to zero
    board = np.zeros((BOARDWIDTH, BOARDHEIGHT), dtype='int')
    return board


def getRandomMove(board):
    # pick a random column number which is Valid
    while True:
        x = random.randint(0, 6)
        if isValidMove(board, x):
            return x


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT - 1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def isValidMove(board, column):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False
    return True


def isBoardFull(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


def isWinner(board, tile):  # Checks if the move was the winning move
    # check horizontal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if board[x][y] == tile and board[x + 1][y] == tile and board[x + 2][y] == tile and board[x + 3][y] == tile:
                return True
    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y + 1] == tile and board[x][y + 2] == tile and board[x][y + 3] == tile:
                return True
    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x + 1][y - 1] == tile and board[x + 2][y - 2] == tile and board[x + 3][
                        y - 3] == tile:
                return True
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x + 1][y + 1] == tile and board[x + 2][y + 2] == tile and board[x + 3][
                        y + 3] == tile:
                return True
    return False


def play_without_ui(agent_1, agent_2):
    # Set up a blank board data structure.
    board = getNewBoard()
    player = 1

    while True:  # main game loop
        if player == 1:
            column = agent_1(board)
        else:
            column = agent_2(board)
        board = makeMove(board, player, column)
        if isWinner(board, player):
            return player
        player *= -1  # switch to other player's turn
        if isBoardFull(board):
            # A completely filled board means it's a tie.
            return 0


def getReward(board, player):
    if isWinner(board, player):
        return 10 * player
    if isBoardFull(board):
        return 5
    return -1


def getNeuralInput(state):
    new_state = state.reshape(1, BOARDHEIGHT*BOARDWIDTH)
    x = np.append((new_state == 0).astype(int), (new_state == 1).astype(int))
    x = np.append(x, (new_state == -1).astype(int))
    return x


if __name__ == '__main__':
    winners = [0, 0, 0]
    for i in range(100000):
        winners[play_without_ui(getRandomMove, getRandomMove)] += 1
    plotResults(winners[1], winners[-1], winners[0])
