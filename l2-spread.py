import math
import itertools
import numpy as np
from sage.all import *
from sage.graphs.graph_coloring import first_coloring

def dist(p,q):
    # compute L2 distance between two points
    return sum([(p[i]-q[i])** 2 for i in range(len(p))])**0.5

def create_graph(points, r):
    # construct distance graph from a set of points
    d = {}
    for i in range(len(points)):
        d[i] = [j for j in range(i+1, len(points)) if dist(points[i], points[j]) > r]
    return Graph(d)

def norm(p):
    # compute L2 norm of a point
    return sum([(p[i])** 2 for i in range(len(p))])**0.5

def spherical_midpoint(lst):
    # construct midpoint/centroid along spherical arc between a list of points
    midpoint = tuple(map(sum, zip(*lst)))
    a = norm(midpoint)
    spherical_midpoint =  tuple(map(lambda x: x/a , midpoint))
    return spherical_midpoint 

def minus(p):
    # reflect a point about the origin
    return tuple([-c for c in p])

def add_same_color_gadget(graph, mono_set):
    # force two special points to have the same color
    N = graph.order()
    graph.add_vertices([N, N+1])
    graph.add_edge(N, N+1)
    for u in mono_set:
        graph.add_edge(N, u)
        graph.add_edge(N+1, u)

def partitions(n, I=1):
    yield (n,)
    for i in range(I, n//2 + 1):
        for p in partitions(n-i, i):
            yield (i,) + p

def pad_infinite(iterable, padding=None):
   return itertools.chain(iterable, itertools.repeat(padding))

def pad(iterable, size, padding=None):
   return itertools.islice(pad_infinite(iterable, padding), size)

def get_all_partitions(n, dims):
    # return all partitions of 'n' into 'dims' many nonzero integers
    all_partitions = [list(pad(list(p), dims, 0)) for p in partitions(n) if len(p) <= dims]
    return [*itertools.chain.from_iterable(set(itertools.permutations(p)) for p in all_partitions)]

def make_positive_region_partition(dims, aspect):
    identity = np.identity(dims).tolist()
    points = []
    for partition in get_all_partitions(aspect, dims):
        partition=list(partition)
        points_to_average = []
        i = 0
        while i < dims:
            if partition[i] >= 1:
                points_to_average.append(identity[i])
                partition[i] -= 1
            else:
                i += 1
        points.append(spherical_midpoint(points_to_average))
    return points

def make_region(root_points, positive_region):
    return positive_region @ np.matrix(root_points)

if __name__ == '__main__':
    # we construct a certain set of points on a sphere, and verify that it satisfies a 'spread property' for a certain threshold r (see README.md for more information)

    granularity = 12 # granularity of partition
    identity = np.identity(3)
    zeros = np.zeros(3)

    root_1 = [identity[0], minus(identity[1]), minus(identity[2])]
    root_2 = [minus(identity[0]), identity[1], minus(identity[2])]
    root_3 = [minus(identity[0]), minus(identity[1]), identity[2]]

    # construct pointset
    positives = make_positive_region_partition(3, granularity)
    region_1 = make_region(root_1, positives)
    region_2 = make_region(root_2, positives)
    region_3 = make_region(root_3, positives)
    identity = np.identity(3).tolist()
    points = np.vstack((np.identity(3), -np.identity(3), region_1, region_2, region_3)).tolist()

    r = 1.3
    increment = 0.001
    active = True
    while active:
        G = create_graph(points, math.sqrt(2)*r)

        add_same_color_gadget(G, [0,1])
        active = not bool(len(first_coloring(G, 3))==3)
        if active:
            print('G is not 3-colorable with r = {:.3f}.'.format(r))
        else:
            print('G is 3-colorable with r = {:.3f}.'.format(r))
        r += increment
