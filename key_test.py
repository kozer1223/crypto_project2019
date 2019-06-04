from modules.sparsegraph import SparseGraph
from modules.hamiltoniankey import HamiltonianKey
from modules.genkey import generate_key

n = 16
key = generate_key(n)
print(key)
degrees = list(key.public_key.degree(v) for v in key.public_key.vertices())
print('degrees', degrees)

print('graph as adjacency matrix')
print(key.public_key.adjacency_matrix())
