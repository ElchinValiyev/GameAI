import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.grid_2d_graph(20, 20)
pos = dict((n, n) for n in G.nodes())


def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


shortestPath = nx.astar_path(G, (0, 0), (19, 19), heuristic=dist)
node_colors = ["red" if n in shortestPath else "black" for n in G.nodes()]
nx.draw(G, pos, node_size=60, alpha=1, node_color=node_colors, with_labels=False)
plt.show()



shortestPath = nx.dijkstra_path(G, (0, 0), (19, 19))
node_colors = ["red" if n in shortestPath else "black" for n in G.nodes()]
nx.draw(G, pos, node_size=60, alpha=1, node_color=node_colors, with_labels=False)

plt.show()
