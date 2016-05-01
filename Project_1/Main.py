import matplotlib.pyplot as plt

import changed_tic_tac_toe as ttt


def draw_histogram(list):
    plt.hist(list)
    plt.title("Game statistics")
    plt.xlabel("Winner")
    plt.ylabel("Frequency")
    plt.show()


if __name__ == '__main__':
    winner = []
    for i in range(0, 10000):
        winner.append(ttt.play()[0])
    draw_histogram(winner)
