import matplotlib.pyplot as plt
import numpy as np
import random

BOARD_WIDTH = 19
BOARD_HEIGHT = 19


def plot_results(red_wins, black_wins, tie, title):
    """Plots pie-chart with tournament results"""
    # Setting up plot variables
    labels = ['Red Wins', 'Black Wins', 'Ties']
    sizes = [red_wins, black_wins, tie]
    colors = ['yellowgreen', 'gold', 'lightskyblue']

    plt.pie(sizes, colors=colors, autopct=lambda pct: "" if pct == 0 else '{p:.2f}% '.format(p=pct), labels=labels,
            shadow=True, startangle=70)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    plt.show()
    print ("number of Player 1 wins ", red_wins)
    print ("number of Player 2 wins ", black_wins)
    print ("number of ties ", tie)


def make_move(board, player, column):
    """Return next state of the board, original board is unchanged"""
    new_board = board.copy()
    # Finding the lowest row for the selected column to place the player
    lowest = get_lowest_empty_space(new_board, column)
    if lowest != -1:
        new_board[column][lowest] = player
    return new_board


def get_new_board():
    """Creates a new board and initialize all fields to zero"""
    board = np.zeros((BOARD_WIDTH, BOARD_HEIGHT), dtype='int')
    return board


def get_random_move(board):
    """Picks a random column number which is Valid"""
    while True:
        x = random.randrange(BOARD_WIDTH)
        if is_valid_move(board, x):
            return x


def get_lowest_empty_space(board, column):
    """Return the row number of the lowest empty row in the given column"""
    for y in range(BOARD_HEIGHT - 1, -1, -1):
        if board[column][y] == 0:  # if cell is empty
            return y
    return -1


def is_valid_move(board, column):
    """Returns True if there is an empty space in the given column. Otherwise returns False"""
    if column < 0 or column >= BOARD_WIDTH or board[column][0] != 0:
        return False
    return True


def is_board_full(board):
    """Returns True if there are no empty spaces anywhere on the board."""
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == 0:  # is cell is empty
                return False
    return True


def is_winner(board, player):
    """Checks if player has won"""
    # check horizontal spaces
    for x in range(BOARD_WIDTH - 3):
        for y in range(BOARD_HEIGHT):
            if board[x][y] == player and board[x + 1][y] == player and board[x + 2][y] == player \
                    and board[x + 3][y] == player:
                return True
    # check vertical spaces
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT - 3):
            if board[x][y] == player and board[x][y + 1] == player and board[x][y + 2] == player \
                    and board[x][y + 3] == player:
                return True
    # check / diagonal spaces
    for x in range(BOARD_WIDTH - 3):
        for y in range(3, BOARD_HEIGHT):
            if board[x][y] == player and board[x + 1][y - 1] == player and board[x + 2][y - 2] == player \
                    and board[x + 3][y - 3] == player:
                return True
    # check \ diagonal spaces
    for x in range(BOARD_WIDTH - 3):
        for y in range(BOARD_HEIGHT - 3):
            if board[x][y] == player and board[x + 1][y + 1] == player and \
                            board[x + 2][y + 2] == player and board[x + 3][y + 3] == player:
                return True
    return False


def play_without_ui(agent_1, agent_2):
    """Runs one game between given agents"""
    # Set up a blank board
    board = get_new_board()
    player = 1

    while True:  # main game loop
        if player == 1:
            column = agent_1(board)
        else:
            column = agent_2(board)
        board = make_move(board, player, column)
        if is_winner(board, player):
            return player
        player *= -1  # switch to other player's turn
        if is_board_full(board):
            # A completely filled board means it's a tie.
            return 0


def get_neural_input(state):
    return state.reshape(1, BOARD_HEIGHT * BOARD_WIDTH)


if __name__ == '__main__':
    winners = [0, 0, 0]
    for i in xrange(10000):
        print ('Game: ' + str(i))
        winners[play_without_ui(get_random_move, get_random_move)] += 1
    plot_results(winners[1], winners[-1], winners[0], 'Random vs Random')
