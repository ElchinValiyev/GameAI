import bayesian_learning as bl
import som
import helper as hp
import os.path

if __name__ == '__main__':
    # STRONGLY recommended to choose q3dm1-path1.csv
    point_maps = ["q3dm1-path1.csv", "q3dm1-path2.csv"]
    map_index = input(
        "Enter:\n0 for q3dm1-path1.csv, \n1 for q3dm1-path2.csv")
    points_filename = point_maps[map_index]
    print points_filename
    state_centers_num = input("Enter number of som centers (reasonable: 40-100, max 1300): ")
    activity_centers_num = input("Enter number of activity centers (reasonable: 40-100, max 1300): ")
    som_iterations_num = input("Enter number of learning som iterations, for this some 10 - 20 is enough: ")
    path_iterations_num = input("Enter number of steps to generate path (e.g 300, 500 ...): ")
    som_centers_filename = "som_centers_" + str(state_centers_num)

    if os.path.isfile(som_centers_filename) == False:  # if there is no yet file with same number of som centers
        print "Learning started"
        som.learn_som(points_filename, state_centers_num, som_iterations_num)  # learn som
        print "Learning finished"

    path = bl.run_bayesian_learning(points_filename, som_centers_filename, activity_centers_num, path_iterations_num)
    data_points = hp.read_points(points_filename)
    hp.plot_points(data_points[:, 0], data_points[:, 1], data_points[:, 2], "original path")
    som_centers = hp.read_points(som_centers_filename)
    hp.plot_points(som_centers[:, 0], som_centers[:, 1], som_centers[:, 2], "som centers")
    hp.plot_points(path[:, 0], path[:, 1], path[:, 2], "generated path")
