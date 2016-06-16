import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# Jump Point Search is approach to improve A star, so we ll need a star self-written anyway
# Here it is :)

def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


A = np.matrix(np.loadtxt("simpleMap-4-22x34.txt"))
B = np.swapaxes(np.flipud(A), 0, 1)
xs, ys = np.where(B == 1)
gr = nx.grid_2d_graph(np.size(B, axis=0), np.size(B, axis=1))

pos = dict((n, n) for n in gr.nodes())

for i in range(xs.size):
    gr.remove_node((xs[i], ys[i]))
direction = {(0, 1), (0, -1), (1, 0), (-1, 0)}

source = (0, 1)
destination = (4, 15)


def reconstruct_path(G, s, t):
    total_path = [t]
    current = t
    while current != s:
        current = G.node[current]['p']
        total_path.append(current)
    return total_path


def a_star(G, s, t):
    closed = []
    fringe = []

    for n in G.node:
        G.node[n]['g'] = np.inf
        G.node[n]['f'] = G.node[n]['g'] + dist(n, t)
        G.node[n]['p'] = -1

    G.node[source]['g'] = 0
    G.node[source]['f'] = G.node[source]['g'] + dist(n, t)
    fringe.append(source)

    while fringe:  # while not empty: not empty == not list_name
        fringe.sort(key=lambda tup: np.min(G.node[tup]['f']))
        u = fringe[0]

        if u == t:
            return reconstruct_path(G, s, t)

        closed.append(u)
        fringe.remove(u)

        neib = G.neighbors(u)
        for n in closed:
            if n in neib:
                neib.remove(n)

        for v in neib:
            newg = G.node[u]['g'] + 1
            if not (n in fringe) or newg < G.node[v]['g']:
                G.node[v]['g'] = newg
                G.node[v]['f'] = G.node[v]['g'] + dist(v, t)
                G.node[v]['p'] = u
                if not (v in fringe):
                    fringe.append(v)

    return None


print a_star(gr, source, destination)

path = a_star(gr, source, destination)
# path = nx.dijkstra_path(gr,source,destination)
node_colors = ["red" if n in path else "black" for n in gr.nodes()]

plt.figure()
nx.draw(gr, pos, node_size=60, alpha=1, with_labels=False, node_color=node_colors)

# plt.figure()
# path2 = nx.astar_path(gr,source,destination,dist)
# list2 = [source,destination]
# node_colors = ["red" if n in path2 else "black" for n in gr.nodes()]
# nx.draw(gr,pos,node_size=60, alpha=1, with_labels=False, node_color = node_colors)
plt.show()
