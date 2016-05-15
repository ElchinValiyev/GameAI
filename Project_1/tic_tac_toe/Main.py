import matplotlib.pyplot as plt

import agent
import changed_tic_tac_toe as ttt
from qlearner import QLearner


def draw_histogram(winner_list, title):
    plt.figure()
    plt.hist(winner_list)
    plt.title(title)
    plt.xlabel("Winner")
    plt.ylabel("Frequency")
    plt.show()


def show_stats(agent_1, agent_2, title):
    winner_list = []
    for i in range(0, 1000):
        winner_list.append(ttt.play(agent_1, agent_2))
    draw_histogram(winner_list, title)


if __name__ == '__main__':
    # random vs probabilistic
    show_stats(agent.get_random_move, agent.get_probabilistic_move, "Random(X) vs Probabilistic(O)")

    # probabilistic vs minmax
    show_stats(agent.get_probabilistic_move, agent.get_minmax_move, "Probabilistic(X) vs Minmax(O)")

    # minmax vs minmax
    show_stats(agent.get_minmax_move, agent.get_minmax_move, "Minmax(X) vs Minmax(O)")

    qlearner = QLearner()
    show_stats(qlearner.get_max_q_move, agent.get_minmax_move, "Q-learning(X) vs Minmax(O)")
