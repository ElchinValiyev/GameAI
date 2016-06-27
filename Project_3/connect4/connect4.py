import matplotlib.pyplot as plt
import numpy as np
import random

BOARDWIDTH = 19
BOARDHEIGHT = 19
EMPTY = 0


def make_autopct(values):
    def my_autopct(pct):
        if pct == 0:
            return ""
        else:
            return '{p:.2f}% '.format(p=pct)

    return my_autopct


def plot_results(red_wins, black_wins, tie, title):
    # Setting up plot variables
    labels = ['Red Wins', 'Black Wins', 'Ties']
    sizes = [red_wins, black_wins, tie]
    colors = ['yellowgreen', 'gold', 'lightskyblue']
    explode = (0.1, 0, 0)

    plt.pie(sizes, colors=colors, autopct=make_autopct(sizes), explode=explode, labels=labels, shadow=True,
            startangle=70)
    plt.axis('equal')
    plt.title(title)
    plt.tight_layout()
    plt.show()
    print "number of red wins ", red_wins
    print "number of black wins ", black_wins
    print "number of ties ", tie


def make_move(board, player, column):
    new_board = board.copy()
    # Finding the lowest row for the selected column to place the player
    lowest = get_lowest_empty_space(new_board, column)
    if lowest != -1:
        new_board[column][lowest] = player
    return new_board


def get_new_board():
    # Create a new board and initilize all fields to zero
    board = np.zeros((BOARDWIDTH, BOARDHEIGHT), dtype='int')
    return board


def get_random_move(board):
    # pick a random column number which is Valid
    while True:
        x = random.randint(0, 6)
        if is_valid_move(board, x):
            return x


def get_lowest_empty_space(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT - 1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1


def is_valid_move(board, column):
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False
    return True


def is_board_full(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


def is_winner(board, tile):  # Checks if the move was the winning move
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
    new_state = state.reshape(1, BOARDHEIGHT * BOARDWIDTH)
    x = np.append((new_state == 0).astype(int), (new_state == 1).astype(int))
    x = np.append(x, (new_state == -1).astype(int))
    return x


if __name__ == '__main__':
    winners = [0, 0, 0]
    for i in range(100000):
        winners[play_without_ui(get_random_move, get_random_move)] += 1
    plot_results(winners[1], winners[-1], winners[0], 'Random vs Random')
