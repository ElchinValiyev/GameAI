import numpy as np
import random


def distance(a, b):
    sum_square = 0
    for i in range(len(a)):
        sum_square += (a[i] - b[i]) ** 2
    return np.sqrt(sum_square)


def e_step(centers, datapoints):
    clusters = np.zeros((len(datapoints)), dtype=np.int64)

    for i in range(len(datapoints)):
        dist = [distance(datapoints[i], k) for k in centers]
        min_index, = np.where(dist == np.min(dist))
        clusters[i] = min_index[0]
    return clusters


def m_step(clusters, datapoints, centers):
    sum = np.zeros(centers.shape)
    counters = np.bincount(clusters)
    for j in range(len(centers)):
        for i in range(len(clusters)):
            if (clusters[i] == j):
                sum[j] = sum[j] + datapoints[i]
        centers[j] = sum[j] / counters[j]
    return centers


def kmeans(k, datapoints):
    centers = np.array(random.sample(datapoints, k))
    clusters = np.zeros((len(datapoints)))
    assert len(centers) == k
    old_centers = np.zeros(np.shape(centers))
    while not((old_centers == centers).all()):
        old_centers = centers
        clusters = e_step(centers, datapoints)
        centers = m_step(clusters, datapoints, centers)
    return clusters, centers
