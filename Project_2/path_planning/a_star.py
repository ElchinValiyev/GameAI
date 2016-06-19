import numpy as np


def distance(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def reconstruct_path(graph, source, target):
    total_path = [target]
    current = target
    while current != source:
        current = graph.node[current]['parent']
        total_path.append(current)
    return total_path


def a_star(graph, source, target):
    closed = []
    fringe = []

    for n in graph.node:
        graph.node[n]['cost'] = np.inf
        graph.node[n]['estimated_distance'] = graph.node[n]['cost'] + distance(n, target)
        graph.node[n]['parent'] = -1

    graph.node[source]['cost'] = 0
    graph.node[source]['estimated_distance'] = graph.node[source]['cost'] + distance(source, target)
    fringe.append(source)

    while fringe:  # while not empty: not empty == not list_name
        fringe.sort(key=lambda tup: np.min(graph.node[tup]['estimated_distance']))
        current = fringe[0]

        if current == target:
            return reconstruct_path(graph, source, target)

        closed.append(current)
        fringe.remove(current)

        neighbours = graph.neighbors(current)
        for n in closed:
            if n in neighbours:
                neighbours.remove(n)

        for node in neighbours:
            new_cost = graph.node[current]['cost'] + 1
            if not (node in fringe) or new_cost < graph.node[node]['cost']:
                graph.node[node]['cost'] = new_cost
                graph.node[node]['estimated_distance'] = graph.node[node]['cost'] + distance(node, target)
                graph.node[node]['parent'] = current
                if not (node in fringe):
                    fringe.append(node)

    return None
