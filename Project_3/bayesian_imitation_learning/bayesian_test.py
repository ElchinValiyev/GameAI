import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from kohonen.kohonen import *
import numpy as np
import csv

with open("q3dm1-path2.csv") as filein:
    # quoting - is needed for conversion to int, since csv reads as strings
    reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    xs, ys, zs = zip(*reader)

input = np.array([xs, ys, zs]).transpose()

som_parameters = Parameters(dimension=3, shape=(1, 40), learning_rate=0.1, neighborhood_size=2, metric=euclidean_metric)
som = Map(som_parameters)
print len(input)
for i in range(len(input)):
    som.learn(input[i])

print som.neurons
plt.figure()
Map.neuron_heatmap(som, axes=(0, 1))
plt.show()
