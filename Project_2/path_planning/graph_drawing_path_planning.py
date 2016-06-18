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
#A = np.matrix(np.loadtxt("simpleDungeonMap.txt"))
B = np.swapaxes(np.flipud(A), 0, 1)
xs, ys = np.where(B == 1)
gr = nx.grid_2d_graph(np.size(B, axis=0), np.size(B, axis=1))

pos = dict((n, n) for n in gr.nodes())

for i in range(xs.size):
    gr.remove_node((xs[i], ys[i]))
direction = {(0, 1), (0, -1), (1, 0), (-1, 0)}

source = (0, 1)
destination = (4, 15)
#source = (3,5)
#destination = (2,18)


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

def has_vertical_blocked(G, node, dir):
    step_before = (node[0]-dir[0],node[1]-dir[1])
    step_before_down = (step_before[0],step_before[1]-1)
    step_before_up = (step_before[0], step_before[1] + 1)
    return not(step_before_down in G.node) or not(step_before_up in G.node)

def has_vertical_obstacle(G, node, dir):
    step_next = (node[0]+dir[0],node[1])

    return not(step_next in G.node)



def jump(G, n, dir, start, goal):

    if not (n in G.node):
        return None
    if n == goal:
        return n
    #horizontal move
    if not dir[0]==0:
        #node below
        node1 = (n[0],n[1]-1)
        #prev node below
        node2 = (n[0]-dir[0],n[1]-1)
        #node above
        node3 = (n[0], n[1] + 1)
        # prev node above
        node4 = (n[0] - dir[0], n[1] + 1)
        if (node1 in G.node and not (node2 in G.node)) or (node3 in G.node and not (node4 in G.node)):
            return n
            # When moving vertically, must check for horizontal jump points
        if jump(G, node1, (0, -1), start, goal) or jump(G, node3, (0, 1), start, goal):
            return n
    #vertical move
    elif not dir[1]==0:
        # node left
        node5 = (n[0]-1, n[1])
        # prev node left
        node6 = (n[0] - 1, n[1] -dir[1])
        # node right
        node7 = (n[0]+1, n[1])
        # prev node right
        node8 = (n[0] - dir[0], n[1] - dir[1])
        if (node5 in G.node and not (node6 in G.node)) or (node7 in G.node and not (node8 in G.node)):
            return n
        # When moving vertically, must check for horizontal jump points
#        if jump(G,node5,(-1,0),start,goal) or jump(G,node7,(1,0),start,goal):
#            return n

    return jump(G,(n[0]+dir[0],n[1]+dir[1]),dir, start,goal)

def find_successors(G, node, start, goal):
    successors = []
    neighbours = []
    dict = []
    parent = G.node[node]['p']

    if (parent and not parent==-1):
        dir = ((-parent[0] + node[0]) / max(abs(-parent[0] + node[0]), 1),
               (-parent[1] + node[1]) / max(abs(-parent[1] + node[1]), 1))
        print 'dir'
        print dir
        if not dir[0]==0:
            if (node[0],node[1]+1) in G.node:
                neighbours.append((node[0],node[1]+1))
            if (node[0], node[1] - 1) in G.node:
                neighbours.append((node[0], node[1] - 1))
            if (node[0]+dir[0], node[1]) in G.node:
                neighbours.append((node[0]+dir[0], node[1]))
        elif not dir[1] == 0:
            if (node[0]+1, node[1]) in G.node:
                neighbours.append((node[0]+1, node[1]))
            if (node[0]-1, node[1]) in G.node:
                neighbours.append((node[0]-1, node[1]))
            if (node[0], node[1]+dir[1]) in G.node:
                neighbours.append((node[0], node[1] + dir[1]))
    else:
        neighbours  = G.neighbors(node)
    print "neibors"
    print neighbours
    for n in neighbours:
        print 'n'
        print n

        dir_xn = (n[0]-node[0], n[1] - node[1])
        print dir_xn
        n = jump(G,n,dir_xn,start,goal)
        print n
        if n:
            successors.append(n)
            dist = max((n[0]-node[0]),(n[1]-node[1]))
            dict.append((n,dist))

    return successors, dict

print "(((((((((((((((((((((((((("

print jump(gr,(3,6),(0,1),source,destination)



def a_star_jps(G, s, t):
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

        neib, dict = find_successors(G,u,s,t)
        print 'point'
        print u
        print "N"
        print neib

        for n in closed:
            if n in neib:
                neib.remove(n)



        for v in neib:
            cost = 0
            for tuple in dict:
                if tuple[0]==v:
                    cost = tuple[1]

            newg = G.node[u]['g'] + cost

            if not (n in fringe) or newg < G.node[v]['g']:
                G.node[v]['g'] = newg
                G.node[v]['f'] = G.node[v]['g'] + dist(v, t)
                G.node[v]['p'] = u
                if not (v in fringe):
                    fringe.append(v)

    return closed






p1 = a_star_jps(gr,source,destination)

path = a_star(gr, source, destination)



# path = nx.dijkstra_path(gr,source,destination)
node_colors = ["red" if n in p1 else "black" for n in gr.nodes()]

plt.figure()
nx.draw(gr, pos, node_size=60, alpha=1, with_labels=False, node_color=node_colors)

# plt.figure()
# path2 = nx.astar_path(gr,source,destination,dist)
# list2 = [source,destination]
# node_colors = ["red" if n in path2 else "black" for n in gr.nodes()]
# nx.draw(gr,pos,node_size=60, alpha=1, with_labels=False, node_color = node_colors)
plt.show()
