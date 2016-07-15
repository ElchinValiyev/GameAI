import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def write_points(xs, ys, zs, output_file):
    with open(output_file, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        points_as_list = [xs.tolist(), ys.tolist(), zs.tolist()]
        points_as_3tuples = zip(*points_as_list)
        for i in range(len(points_as_3tuples)):
            csv_writer.writerow(points_as_3tuples[i])


def read_points(input_file):
    with open(input_file) as filein:
        # quoting - is needed for conversion to int, since csv reads as strings
        reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
        xs, ys, zs = zip(*reader)

    return np.array([xs, ys, zs]).transpose()


def plot_points(xs, ys, zs, title):
    ax = plt.axes(projection='3d')
    ax.set_xlim3d(0, 1200)
    ax.set_ylim3d(1800, 2400)
    ax.set_zlim3d(20, 45)

    ax.scatter(xs, ys, zs)
    plt.title(title)

    plt.show(block=True)
