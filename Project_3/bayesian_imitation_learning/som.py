from task3 import SOM
import helper as hp
import numpy as np


def learn_som(input_file, centers_number, iterations_number):
    som1 = SOM(centers_number)
    points = hp.read_points(input_file)
    xs, ys, zs = points[:, 0], points[:, 1], points[:, 2]
    for iteration in range(1, iterations_number):
        for i in range(0, len(xs)):
            som1.update(xs[i], ys[i], zs[i], iteration, iterations_number)
            # som1.som_print()
        somx = []
        somy = []
        somz = []
        for i in range(0, len(som1.list)):
            somx.append(som1.list[i].x)
            somy.append(som1.list[i].y)
            somz.append(som1.list[i].z)

    output_file = "som_centers_" + str(centers_number)
    hp.write_points(np.array(somx), np.array(somy), np.array(somz), output_file)

    return somx, somy, somz
