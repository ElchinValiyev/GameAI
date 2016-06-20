import numpy as np


def distance(a, b):  # Euclidean distance
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def reconstruct_path(graph, source, target):  # reconstructs path from source to target
    total_path = [target]
    current = target
    while current != source:
        current = graph.node[current]['parent']
        total_path.append(current)
    return total_path


def a_star(graph, source, target):
    closed = []
    fringe = []

    # set costs and estimated distances to infinity, parent nodes to -1 for all nodes
    for n in graph.node:
        graph.node[n]['cost'] = np.inf
        graph.node[n]['estimated_distance'] = graph.node[n]['cost'] + distance(n, target)
        graph.node[n]['parent'] = -1

    # only for source set cost to zero, estimated distance to distance between source and targe
    graph.node[source]['cost'] = 0
    graph.node[source]['estimated_distance'] = graph.node[source]['cost'] + distance(source, target)
    # put to fringe
    fringe.append(source)

    while fringe:  # while fringe not empty: not empty == not list_name
        fringe.sort(key=lambda tup: np.min(graph.node[tup]['estimated_distance']))
        current = fringe[0]# tak one with best estimated distance

        if current == target:  # if target, we are ready
            return reconstruct_path(graph, source, target)  # return path from source to target

        closed.append(current)  # put to closed
        fringe.remove(current)  # remove from fringe

        neighbours = graph.neighbors(current)  # get neighbours
        for n in closed:  # delete those that are already closed
            if n in neighbours:
                neighbours.remove(n)

        for node in neighbours:  # for each neighbour
            new_cost = graph.node[current]['cost'] + 1  # calculate new cost
            # if not in fringe or new cost better then previous
            # set new cost, recalculate distance, set parent to current node
            if not (node in fringe) or new_cost < graph.node[node]['cost']:
                graph.node[node]['cost'] = new_cost
                graph.node[node]['estimated_distance'] = graph.node[node]['cost'] + distance(node, target)
                graph.node[node]['parent'] = current
                if not (node in fringe):  # if yet not in fringe, put
                    fringe.append(node)

    return None
