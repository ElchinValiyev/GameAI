import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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







fig = plt.figure()




xa = som.neurons[:, :, 0].flatten()
ya = som.neurons[:, :, 1].flatten()
za = som.neurons[:, :, 2].flatten()

ax = plt.axes(projection='3d')

ax.scatter(xa, ya, za)


#im = plt.imshow(ax, cmap=plt.get_cmap('viridis'), animated=True)
def update_som(som):
    for i in range(len(map_input)):
        som.activate(map_input[i])
        som.backward()
    return som




def updatefig(i,som,ax):
    som.activate(map_input[i])
    som.backward()
    xa = som.neurons[:, :, 0].flatten()
    ya = som.neurons[:, :, 1].flatten()
    za = som.neurons[:, :, 2].flatten()
    sc = ax.scatter(xa,ya,za)
    return sc,


numframes = 10


ani = animation.FuncAnimation(fig, updatefig, frames=xrange(numframes), fargs=(som, ax))
plt.show()