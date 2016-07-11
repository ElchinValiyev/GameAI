'''
Created on 12 June 2016

@author: Maxim Maltsev
'''
#file parsing and computing a tree based on array
text_file = open("D:/task2_tree.txt", "r")
lines = text_file.read().split('\n')
tree = []
for i in xrange(len(lines)):
    element = lines[i].split(" ")
    for i in xrange(len(element)):
        element[i] = float(element[i])
    tree.append(element)

def minimax(node, depth, if_max):
    if depth == 0: #termination level
        return tree[node][node] #the value of node

    if if_max:
        best_value = -float('INF')
        for i in xrange(len(tree[node])):
            if tree[node][i] > 0: #for each child of node
                child_value = minimax(i, depth-1, 0)
                best_value = max(best_value, child_value)
        return best_value

    else:    #minimizing player
        best_value = float('INF')
        for i in xrange(len(tree[node])):
            if tree[node][i] > 0: #for each child of node
                child_value = minimax(i, depth-1, 1)
                best_value = min(best_value, child_value)
        return best_value

result = minimax(0, 3, 1) #node, depth, if_max
print(result)