import graph_constructor
import a_star_jps
import a_star
import networkx as nx

if __name__ == '__main__':
    maps = ["simpleDungeonMap.txt", "simpleMap-4-22x34.txt", "test_map.txt", "simpleMap-1-20x20.txt"]
    map_index = input(
        "Enter:\n0 for dungeon rooms \n1 for toughest map here \n2 for our map \n3 for simplest map: \n")
    map = maps[map_index]
    graph = graph_constructor.construct_graph(map)
    # some possible sources and destinations
    if map_index == 0:
        source = (3, 5)
        target = (2, 18)
    elif map_index == 1:
        source = (0, 1)
        target = (34, 20)
    elif map_index == 2:
        source = (3, 9)
        target = (30, 9)
    elif map_index == 3:
        source = (0, 10)
        target = (15, 1)

    directions = ["vertical", "horizontal"]

    direction_index = input("Enter preferred direction for jump point search: \n0 for vertical, \n1 for horizonal \n")

    direction = directions[direction_index]

    dijkstra_path = nx.dijkstra_path(graph, source, target)

    graph_constructor.draw_path(graph, dijkstra_path, "Dijkstra")

    a_star_path = a_star.a_star(graph, source, target)

    graph_constructor.draw_path(graph, a_star_path, "A Star")

    jps_path = a_star_jps.a_star_jps(graph, source, target, direction)

    graph_constructor.draw_path(graph, jps_path, "Jump Point Search")
