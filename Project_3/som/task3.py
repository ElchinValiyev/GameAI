from __future__ import division
import random
import matplotlib.pyplot as plt
from pylab import figure, axes, pie, title, show
from mpl_toolkits.mplot3d import Axes3D
import csv
import math
import numpy as np
import matplotlib.cm as cm

class Neuron:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SOM:

    list = []
    def __init__(self, card):
        for i in range (0,card):
            self.list.append(Neuron(random.randint(0,1000), random.randint(0, 2000), random.randint(0, 100)))

    def calculate_winner(self, x, y, z):
        distance_to_point = []
        min_distance_to_point = 1000
        winner = 0
        for i in range(0, len(self.list)):
            dist = math.sqrt(pow(self.list[i].x - x, 2) + pow(self.list[i].y - y, 2) + pow(self.list[i].z - z, 2))
            distance_to_point.append(dist)
            if abs(dist) < min_distance_to_point:
                min_distance_to_point = dist
                winner = i
        return winner

    def update (self, x, y, z, iteration, number_of_iterations):
        nyu = 1 / 10
        winner = self.calculate_winner(x, y, z)
        for i in range(0, len(self.list)):
            deltax = nyu * pow(number_of_iterations, 1 / (iteration+1)) * (pow(1 - list_distance(self.list, winner, i) / len(self.list), 20)) * (x - self.list[i].x)
            deltay = nyu * pow(number_of_iterations, 1 / (iteration+1)) * (pow(1 - list_distance(self.list, winner, i) / len(self.list), 20)) * (y - self.list[i].y)
            deltaz = nyu * pow(number_of_iterations, 1 / (iteration+1)) * (pow(1 - list_distance(self.list, winner, i) / len(self.list), 20)) * (z - self.list[i].z)
            self.list[i].x += deltax
            self.list[i].y += deltay
            self.list[i].z += deltaz

    def som_print(self):
        for i in range (0, len(self.list)):
            print self.list[i].x, self.list[i].y , self.list[i].z

        print '______'


def list_distance(list, ind1, ind2):
    max_ind = max(ind1, ind2)
    min_ind = min(ind1, ind2)
    dist = min(len(list) - max_ind + min_ind, max_ind - min_ind)
    return dist



som1 = SOM(20)
som1.som_print()

with open("q3dm1-path2.csv") as filein:
    # quoting - is needed for conversion to int, since csv reads as strings
    reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    xs, ys, zs = zip(*reader)
    number_of_iterations = 15
    for iteration in range (1, number_of_iterations):
        for i in range(0, len(xs)):
            som1.update(xs[i], ys[i], zs[i], iteration, number_of_iterations)
        som1.som_print()
        somx = []
        somy = []
        somz = []
        for i in range(0, len(som1.list)):
            somx.append(som1.list[i].x)
            somy.append(som1.list[i].y)
            somz.append(som1.list[i].z)
        plt.style.use('ggplot')
        ax = plt.axes(projection='3d')
        ax.scatter(xs, ys, zs)
        ax.scatter(somx, somy, somz, c = 'r', s = 50)
        #plt.savefig('test' + str(iteration) + '.png')
        plt.show()


