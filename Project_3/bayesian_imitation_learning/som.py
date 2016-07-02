import pylab
import matplotlib.pyplot as plt
from scipy import random
from pybrain.structure.modules import KohonenMap
import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


som = KohonenMap(3, 8)
print som.neurons

with open("q3dm1-path2.csv") as filein:
    # quoting - is needed for conversion to int, since csv reads as strings
    reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    xs, ys, zs = zip(*reader)

map_input = np.array([xs,ys,zs]).transpose()
for j in range(150):
    #print j
    for i in range(len(map_input)):
        som.activate(map_input[i])
        som.backward()
        xa = som.neurons[:, :, 0].flatten()
        ya = som.neurons[:, :, 1].flatten()
        za = som.neurons[:, :, 2].flatten()

        ax = plt.axes(projection='3d')

        ax.scatter(xa,ya,za)

        plt.show(block=True)

#pylab.ion()






