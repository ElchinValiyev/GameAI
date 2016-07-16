from __future__ import division
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy
import random
import matplotlib.pyplot as plt
import csv
import math


class Neuron:  # class that contains the coordinates of the each neuron of SOM

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SOM:

    list = []  # list of the SOM neurons
    def __init__(self, card):  # SOM initialization by randomly choosing (card) points
        for i in range (0,card):
            self.list.append(Neuron(random.randint(0,1500), random.randint(1500, 2600), random.randint(0, 100)))

    def calculate_winner(self, x, y, z):  # finding the closest meuron to the chosen point from the dataset
        distance_to_point = []
        min_distance_to_point = 1000
        winner = 0
        for i in range(0, len(self.list)):
            dist = math.sqrt(pow(self.list[i].x - x, 2) + pow(self.list[i].y - y, 2) + pow(self.list[i].z - z, 2))  # dist. is measured by Euclidean distance metric
            distance_to_point.append(dist)
            if abs(dist) < min_distance_to_point:
                min_distance_to_point = dist
                winner = i
        return winner

    def update (self, x, y, z, iteration, number_of_iterations):
        nyu = 1 / 30  # learning rate
        winner = self.calculate_winner(x, y, z)  # index of the closest neuron to the point
        for i in range(0, len(self.list)):
            deltax = nyu * pow(number_of_iterations, 1 / (iteration+1)) * (pow(1 - list_distance(self.list, winner, i) / len(self.list), 15)) * (x - self.list[i].x)
            deltay = nyu * pow(number_of_iterations, 1 / (iteration+1)) * (pow(1 - list_distance(self.list, winner, i) / len(self.list), 15)) * (y - self.list[i].y)
            deltaz = nyu * pow(number_of_iterations, 1 / (iteration+1)) * (pow(1 - list_distance(self.list, winner, i) / len(self.list), 15)) * (z - self.list[i].z)
            self.list[i].x += deltax  # shifting the neuron by delta
            self.list[i].y += deltay
            self.list[i].z += deltaz

    def som_print(self):  # printing the result into console
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
list_prev = []

with open("q3dm1-path2.csv") as filein:
    # quoting - is needed for conversion to int, since csv reads as strings
    reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    xs, ys, zs = zip(*reader)  # lists with the given dataset
    number_of_iterations = 5  # number of the iterations of learning (chosen by the user)
    for iteration in range (1, number_of_iterations):
        list_prev = deepcopy(som1.list)  # saving the previous list of neurons for showing the diffrence on the picture
        for i in range(0, len(xs)):  # updating the list of neurons accorfing to the dataset
            som1.update(xs[i], ys[i], zs[i], iteration, number_of_iterations)
    # --- Drawing plots --- #
        som1.som_print()
        somx = []  #
        somy = []
        somz = []
        for i in range(0, len(som1.list)):
            somx.append(list_prev[i].x)
            somy.append(list_prev[i].y)
            somz.append(list_prev[i].z)
        somx.append(list_prev[0].x)
        somy.append(list_prev[0].y)
        somz.append(list_prev[0].z)
        for j in range(0, len(list_prev)):
            list_prev[j] = som1.list[j]
            somx[j] = som1.list[j].x
            somy[j] = som1.list[j].y
            somz[j] = som1.list[j].z
            if j == 0:
                somx[len(somx)-1] = som1.list[0].x
                somy[len(somy)-1] = som1.list[0].y
                somz[len(somz)-1] = som1.list[0].z
            plt.style.use('ggplot')
            ax = plt.axes(projection='3d')
            ax.scatter(xs, ys, zs)
            ax.scatter(list_prev[j].x, list_prev[j].y, list_prev[j].z, c = 'k', s = 200)
            ax.plot(somx, somy, somz, '-o')
            plt.savefig('plot' + str(iteration) + '_' + str(j) + '.png')
            #plt.show()

    # --- Writing results into .csv file --- #
    file_creator = open('result.csv', 'w')
    file_writer = csv.writer(file_creator)
    for j in range(0, len(som1.list)):
        file_writer.writerow((som1.list[j].x,som1.list[j].y,som1.list[j].z))
    file_creator.close()