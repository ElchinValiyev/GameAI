import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def dist(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def remove_positions(graph, file_name):
    data = np.loadtxt(file_name)
    adjacency_matrix = np.swapaxes(np.flipud(data))
    x, y = np.where(adjacency_matrix==1)
    graph.remove_node((x[:],y[:]))


A=np.loadtxt("simpleMap-1-20x20.txt")
B = np.swapaxes(np.flipud(A),0,1)
xs,ys = np.where(B==1)
gr = nx.grid_2d_graph(len(A), len(A))

pos = dict((n, n) for n in gr.nodes())

gr.remove_node((xs[:],ys[:]))

source = (0,10)
destination = (15,1)
path = nx.dijkstra_path(gr,source,destination)
node_colors = ["red" if n in path else "black" for n in gr.nodes()]

plt.figure()
nx.draw(gr,pos,node_size=60, alpha=1, with_labels=False, node_color = node_colors)

plt.figure()
path2 = nx.astar_path(gr,source,destination,dist)
list2 = [source,destination]
node_colors = ["red" if n in path2 else "black" for n in gr.nodes()]
nx.draw(gr,pos,node_size=60, alpha=1, with_labels=False, node_color = node_colors)
#nx.draw(gr,pos,node_size=60, alpha=1, with_labels=False, node_color = node_colors)
plt.show()



#nx.add_nodes_from(H)