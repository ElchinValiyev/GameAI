import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def construct_graph(file_name):
    adjacency_matrix = np.matrix(np.loadtxt(file_name))
    adjacency_matrix_turned = np.swapaxes(np.flipud(adjacency_matrix), 0, 1)
    xs, ys = np.where(adjacency_matrix_turned == 1)
    graph = nx.grid_2d_graph(np.size(adjacency_matrix_turned, axis=0), np.size(adjacency_matrix_turned, axis=1))

    for i in range(xs.size):
        graph.remove_node((xs[i], ys[i]))
    return graph


def draw_path(graph, path, title):
    pos = dict((n, n) for n in graph.nodes())
    node_colors = ["yellow" if n in path else "black" for n in graph.nodes()]
    plt.figure()

    nx.draw(graph, pos, node_size=60, alpha=1, with_labels=False, node_color=node_colors, title=title)
    plt.show()
