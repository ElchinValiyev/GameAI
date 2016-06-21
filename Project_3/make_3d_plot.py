import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

plt.style.use('ggplot') # beautiful style as in R

with open("q3dm1-path2.csv") as filein:
    # quoting - is needed for conversion to int, since csv reads as strings
    reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
    xs, ys, zs = zip(*reader)

# fig = plt.figure() # not necessary, this creates new window
ax = plt.axes(projection='3d')
ax.scatter(xs, ys, zs)

plt.show()
