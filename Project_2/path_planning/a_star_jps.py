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


def jump(graph, current, direction, start, goal, pref_direction):
    if not (current in graph.node):
        return None
    if current == goal:
        return current

    if not direction[0] == 0:  # horizontal move
        if is_horizontal_obstacle(graph, current, direction):
            return current
        if pref_direction == 'horizontal':  # when moving horizontally, must check for vertical jump points
            if jump(graph, (current[0], current[1] - 1), (0, -1), start, goal, pref_direction) or jump(graph, (
            current[0], current[1] + 1), (0, 1), start, goal, pref_direction):
                return current

    elif not direction[1] == 0:  # vertical move
        if is_vertical_obstacle(graph, current, direction):
            return current

        if pref_direction == 'vertical':  # When moving vertically, must check for horizontal jump points
            if jump(graph, (current[0] - 1, current[1]), (-1, 0), start, goal, pref_direction) or jump(graph, (
                current[0] + 1, current[1]), (1, 0), start, goal, pref_direction):
                return current

    return jump(graph, (current[0] + direction[0], current[1] + direction[1]), direction, start, goal, pref_direction)


def find_neighbours(graph, node, start, goal):
    neighbours = []

    parent = graph.node[node]['parent']

    if parent and not parent == -1:
        dir = ((-parent[0] + node[0]) / max(abs(-parent[0] + node[0]), 1),
               (-parent[1] + node[1]) / max(abs(-parent[1] + node[1]), 1))

        if not dir[0] == 0:
            if (node[0], node[1] + 1) in graph.node:
                neighbours.append((node[0], node[1] + 1))
            if (node[0], node[1] - 1) in graph.node:
                neighbours.append((node[0], node[1] - 1))
            if (node[0] + dir[0], node[1]) in graph.node:
                neighbours.append((node[0] + dir[0], node[1]))
        elif not dir[1] == 0:
            if (node[0] + 1, node[1]) in graph.node:
                neighbours.append((node[0] + 1, node[1]))
            if (node[0] - 1, node[1]) in graph.node:
                neighbours.append((node[0] - 1, node[1]))
            if (node[0], node[1] + dir[1]) in graph.node:
                neighbours.append((node[0], node[1] + dir[1]))
    else:
        neighbours = graph.neighbors(node)

    return neighbours


def find_successors(graph, node, start, target, pref_direction):
    successors = []
    costs = []
    neighbours = find_neighbours(graph, node, start, target)
    if neighbours:
        for n in neighbours:
            dir_xn = (n[0] - node[0], n[1] - node[1])
            n = jump(graph, n, dir_xn, start, target, pref_direction)
            if n:
                successors.append(n)
                dist = max(abs((n[0] - node[0])), abs((n[1] - node[1])))
                costs.append((n, dist))

        return successors, costs


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

        successors, costs = find_successors(graph, current, source, target, pref_direction)

        for n in closed:
            if n in successors:
                successors.remove(n)

        for node in successors:
            cost = 0
            for tup in costs:
                if tup[0] == node:
                    cost = tup[1]

            new_cost = graph.node[current]['cost'] + cost

            if not (node in fringe) or new_cost < graph.node[node]['cost']:
                graph.node[node]['cost'] = new_cost
                graph.node[node]['estimated_distance'] = graph.node[node]['cost'] + distance(node, target)
                graph.node[node]['parent'] = current
                if not (node in fringe):
                    fringe.append(node)

    return None
