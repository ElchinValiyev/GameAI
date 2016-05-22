import matplotlib.pyplot as plt

import agent
import changed_tic_tac_toe as ttt


def make_autopct(values):
    def my_autopct(pct):
        if pct == 0:
            return ""
        else:
            return '{p:.1f}% '.format(p=pct)

    return my_autopct


def draw_chart(winner_list, title):
    plt.title(title)
    labels = ['X Wins', 'O Wins', 'Draw']
    sizes = [winner_list[1], winner_list[-1], winner_list[0]]
    colors = ['yellowgreen', 'gold', 'lightskyblue']
    patches = plt.pie(sizes, colors=colors, autopct=make_autopct(sizes), shadow=True, startangle=90)
    plt.legend(patches[0], labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def show_stats(agent_1, agent_2, title):
    winner_list = [0, 0, 0]  # draw, X, O
    winner = 0
    for i in range(0, 1000):
        winner = ttt.play(agent_1, agent_2)
        winner_list[winner] += 1
    draw_chart(winner_list, title)


if __name__ == '__main__':

    # random vs random
    show_stats(agent.get_random_move, agent.get_random_move, "Random(X) vs Random(O)")

    # probabilistic vs random
    show_stats(agent.get_probabilistic_move, agent.get_random_move, "Probabilistic(X) vs Random(O)")

    # random vs probabilistic
    show_stats(agent.get_random_move, agent.get_probabilistic_move, "Random(X) vs Probabilistic(O)")

    # minmax vs random
    show_stats(agent.get_minmax_move, agent.get_random_move, "Minmax(X) vs Random(O)")

    # minmax vs minmax
    show_stats(agent.get_minmax_move, agent.get_minmax_move, "Minmax(X) vs Minmax(O)")
