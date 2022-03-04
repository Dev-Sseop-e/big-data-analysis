import sys
import numpy as np
from pyspark import SparkConf, SparkContext

f = open(sys.argv[1], 'r')
lines = f.readlines()
dataset = []

# split by the space " "
for line in lines:
    dataset.append(list(map(float, line.split(" "))))

k_val = int(sys.argv[2])    # set the k value
f.close()

def distance(x, y):
    assert len(x) == len(y)
    return np.linalg.norm(np.array(x)-np.array(y))

def find_min(x, sets):
    min_d = -1  # set initial value
    ind = 0
    for y in sets:
        d = distance(x, y)
        if (min_d > d) or (min_d == -1):
            min_d = d
            ind = sets.index(y)
    return (min_d, ind) # return minimum distance and its index

def find_max(x, sets):
    max_d = 0   # set initial value
    for y in sets:
        d = distance(x, y)
        if max_d < d:
            max_d = d
    return max_d    # return maximum distance

def sum(cluster):
    sum_dia = 0
    for c in cluster:
        dia = 0
        sets = c[1]
        for x in sets:
            max = find_max(x, sets)
            if dia < max:
                dia = max
        sum_dia += dia
    return sum_dia  # return the sum of diameters

centroid_set = []
centroid_set.append(dataset[0]) # set the first point

while (len(centroid_set) < k_val):
    centroid_d = 0
    for x in dataset:
        d = find_min(x, centroid_set)[0]
        if centroid_d < d:
            centroid_d = d  # set the centroid distance
            centroid_p = x  # set the centroid point
    centroid_set.append(centroid_p) # append the point

conf = SparkConf()
sc = SparkContext(conf=conf)
sc2 = sc.parallelize(dataset)
# map the clusters
cluster = sc2.map(lambda x: (find_min(x, centroid_set)[1], x)) \
            .groupByKey() \
            .mapValues(list) \
            .collect()

sc.stop()
# calculate and print the average diameter
print ("%f" % (sum(cluster)/k_val))