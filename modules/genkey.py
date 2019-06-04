from .hamiltoniankey import HamiltonianKey
import numpy as np
import itertools
import random
import math

'''
generate_key(n)

Generates HamiltonianKey with n vertices.
'''
def generate_key(n):
    key = HamiltonianKey(n)

    # generate hamiltonian cycle
    cycle = np.random.permutation(n)
    for (i, j) in ((cycle[i], cycle[(i+1) % n]) for i in range(n)):
        key.public_key.add_edge(i, j)

    key.private_key = tuple(cycle)

    # add at least one edge per vertex
    for i in range(n):
        free_vertices = list(j for (i, j) in
            itertools.product((i,), range(n))
            if (i, j) not in key.public_key and i != j)
        if free_vertices:
            j = random.choice(free_vertices)
            key.public_key.add_edge(i, j)

    # try adding extra edges
    for _ in range(int(math.log2(n))):
        u = random.randrange(n)
        v = random.randrange(n - 1)
        if (v >= u):
            v = v + 1
        key.public_key.add_edge(u, v)

    return key
