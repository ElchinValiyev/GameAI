import numpy as np


def distance(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def reconstruct_path(G, source, target):
    total_path = [target]
    current = target
    while current != source:
        current = G.node[current]['parent']
        total_path.append(current)
    return total_path


# detects corner of obstacle that lies front or back
def is_horizontal_obstacle(graph, node, direction):
    node1 = (node[0], node[1] - 1)  # lower neighbour

    node2 = (node[0] - direction[0], node[1] - 1)  # parent's lower neighbour

    node3 = (node[0], node[1] + 1)  # upper neighbour

    node4 = (node[0] - direction[0], node[1] + 1)  # parent's lower neighbou
    return (node1 in graph.node and not (node2 in graph.node)) or (node3 in graph.node and not (node4 in graph.node))


# detects corner of obstacle that lies right or left
def is_vertical_obstacle(graph, node, direction):
    node5 = (node[0] - 1, node[1])  # left neighbour

    node6 = (node[0] - 1, node[1] - direction[1])  # parent's left neighbour

    node7 = (node[0] + 1, node[1])  # right neighbour

    node8 = (node[0] + 1, node[1] - direction[1])  # parent'sleft neighbour
    return (node5 in graph.node and not (node6 in graph.node)) or (node7 in graph.node and not (node8 in graph.node))


def jump(graph, current, direction, source, target, pref_direction):
    if not (current in graph.node):  # if obstacle or end of the grid
        return None
    if current == target:
        return current

    if not direction[0] == 0:  # horizontal move
        if is_horizontal_obstacle(graph, current, direction):  # if obstacle detected
            return current
        if pref_direction == 'horizontal':  # when moving horizontally, must check for vertical jump points
            if jump(graph, (current[0], current[1] - 1), (0, -1), source, target, pref_direction) or jump(graph, (
                    current[0], current[1] + 1), (0, 1), source, target, pref_direction):
                return current

    elif not direction[1] == 0:  # vertical move
        if is_vertical_obstacle(graph, current, direction):
            return current

        if pref_direction == 'vertical':  # when moving vertically, must check for horizontal jump points
            if jump(graph, (current[0] - 1, current[1]), (-1, 0), source, target, pref_direction) or jump(graph, (
                        current[0] + 1, current[1]), (1, 0), source, target, pref_direction):
                return current
    # recursive check for the next step on the grid
    return jump(graph, (current[0] + direction[0], current[1] + direction[1]), direction, source, target,
                pref_direction)


def find_neighbours(graph, node):
    neighbours = []

    parent = graph.node[node]['parent']

    if parent and not parent == -1:  # if node has a parent
        # calculate direction
        dir = ((-parent[0] + node[0]) / max(abs(-parent[0] + node[0]), 1),
               (-parent[1] + node[1]) / max(abs(-parent[1] + node[1]), 1))

        if not dir[0] == 0:  # if horizontal move, append upper, down and next neighbour in direction
            if (node[0], node[1] + 1) in graph.node:
                neighbours.append((node[0], node[1] + 1))
            if (node[0], node[1] - 1) in graph.node:
                neighbours.append((node[0], node[1] - 1))
            if (node[0] + dir[0], node[1]) in graph.node:
                neighbours.append((node[0] + dir[0], node[1]))
        elif not dir[1] == 0:  # if vertical move, append, left, right, and next neighbour in direction
            if (node[0] + 1, node[1]) in graph.node:
                neighbours.append((node[0] + 1, node[1]))
            if (node[0] - 1, node[1]) in graph.node:
                neighbours.append((node[0] - 1, node[1]))
            if (node[0], node[1] + dir[1]) in graph.node:
                neighbours.append((node[0], node[1] + dir[1]))
    else:
        neighbours = graph.neighbors(node)  # if no parent (source), just use built-ins :)

    return neighbours


def find_successors(graph, node, source, target, pref_direction):
    successors = []
    costs = []
    neighbours = find_neighbours(graph, node)
    if neighbours:  # if neighbours not null
        for n in neighbours:  # for each, check for jump point
            dir_xn = (n[0] - node[0], n[1] - node[1])  # in direction from node to its neighbour
            n = jump(graph, n, dir_xn, source, target, pref_direction)
            if n:  # if jump point exist
                successors.append(n)  # put to successors
                dist = max(abs((n[0] - node[0])), abs((n[1] - node[1])))
                costs.append((n, dist))  # put cost of jump between node and this successor

        return successors, costs


# a star, extended with jump point search
def a_star_jps(graph, source, target, pref_direction):
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
        # instead of neighbours, get successors - possible jump points
        successors, costs = find_successors(graph, current, source, target, pref_direction)

        for n in closed:
            if n in successors:
                successors.remove(n)

        for node in successors:  # for each successor
            cost = 0
            for tup in costs:  # get cost
                if tup[0] == node:
                    cost = tup[1]

            new_cost = graph.node[current][
                           'cost'] + cost  # update cost value, not + 1 step, but plus number of steps between current and jump point

            if not (node in fringe) or new_cost < graph.node[node]['cost']:
                graph.node[node]['cost'] = new_cost

                graph.node[node]['estimated_distance'] = graph.node[node]['cost'] + distance(node, target)
                graph.node[node]['parent'] = current
                if not (node in fringe):
                    fringe.append(node)

    return None
