import matplotlib.pyplot as plt
from pybrain.structure.modules import KohonenMap
import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def read_points(input_file):
    with open(input_file) as filein:
        # quoting - is needed for conversion to int, since csv reads as strings
        reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
        xs, ys, zs = zip(*reader)
        print np.array([xs, ys, zs]).transpose()

    return np.array([xs, ys, zs]).transpose()


def learn_som(points_as_matrix, square_root_som_size):
    # 3 is dimension of data point, e.g. if second argument is 5, you will get som of 25 neurons
    som = KohonenMap(3, square_root_som_size)
    for j in range(100):  # for 100 iterations
        print "\r " + str(j)
        for i in range(len(points_as_matrix)):
            som.activate(points_as_matrix[i])
            som.backward()

    center_xs = som.neurons[:, :, 0].flatten()
    center_ys = som.neurons[:, :, 1].flatten()
    center_zs = som.neurons[:, :, 2].flatten()
    return center_xs, center_ys, center_zs


def write_points(xs, ys, zs):
    with open('som_centers.csv', 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        points_as_list = [xs.tolist(), ys.tolist(), zs.tolist()]
        points_as_3tuples = zip(*points_as_list)
        for i in range(len(points_as_3tuples)):
            csv_writer.writerow(points_as_3tuples[i])


def plot_points(xs, ys, zs):
    ax = plt.axes(projection='3d')
    ax.scatter(xs, ys, zs)
    plt.show(block=True)

