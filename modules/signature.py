from .sparsegraph import SparseGraph
from .hamiltoniankey import HamiltonianKey
from .commitment import *
from Crypto.Hash import SHAKE128
import random

k = 64

def sign(m, key):
    if not key.private_key or len(key.private_key) != key.public_key.n:
        raise Exception('invalid private key')

    n = key.public_key.n

    # create boxes
    rounds_data = []
    for t in range(k):
        permutation = generate_perm(n)

        perm_commitments = [commit(v) for v in permutation]
        perm_boxes = [c for (c, r) in perm_commitments]
        perm_keys = [r for (c, r) in perm_commitments]

        graph_boxes = {}
        graph_keys = {}

        inv_permutation = inv(permutation)
        for i in range(n):
            for j in range(i+1, n):
                c, r = commit(key.public_key[(inv_permutation[i], inv_permutation[j])])
                graph_boxes[(i, j)] = c
                graph_keys[(i, j)] = r

        rounds_data.append(
            (permutation, perm_boxes, perm_keys, graph_boxes, graph_keys)
        )

    # create hash
    shake = SHAKE128.new()
    for (permutation, perm_boxes, perm_keys, graph_boxes, graph_keys) in rounds_data:
        shake.update(str(perm_boxes).encode())
        shake.update(str(graph_boxes).encode())
    shake.update(str(m).encode())
    H = shake.read(k // 8)

    # create output
    # keys for boxes
    rounds_keys = []
    for (t, data) in zip(range(k), rounds_data):
        (permutation, perm_boxes, perm_keys, graph_boxes, graph_keys) = data
        bit = get_bit(H, t)

        if bit:
            # 1
            keys = []
            priv_key = key.private_key
            for i in range(n):
                u, v = permutation[priv_key[i]], permutation[priv_key[(i+1) % n]]
                if u > v:
                    u, v = v, u
                graph_key = graph_keys[(u, v)]
                keys.append((u, v, graph_key))
        else:
            # 0
            keys = []
            for i in range(n):
                keys.append((permutation[i], perm_keys[i]))
            inv_permutation = inv(permutation)
            for i in range(n):
                for j in range(i+1, n):
                    keys.append(graph_keys[(i, j)])
        rounds_keys.append(keys)

    round_perm_boxes = [perm_boxes for (permutation, perm_boxes, perm_keys, graph_boxes, graph_keys) in rounds_data]
    round_graph_boxes = [graph_boxes for (permutation, perm_boxes, perm_keys, graph_boxes, graph_keys) in rounds_data]
    return (round_perm_boxes, round_graph_boxes, rounds_keys)

def verify_sign(m, key, signature):
    n = key.public_key.n
    (round_perm_boxes, round_graph_boxes, rounds_keys) = signature

    shake = SHAKE128.new()
    for (perm_boxes, graph_boxes) in zip(round_perm_boxes, round_graph_boxes):
        shake.update(str(perm_boxes).encode())
        shake.update(str(graph_boxes).encode())
    shake.update(str(m).encode())
    H = shake.read(k // 8)

    try:
        for t in range(k):
            perm_boxes = round_perm_boxes[t]
            graph_boxes = round_graph_boxes[t]
            keys = rounds_keys[t]

            bit = get_bit(H, t)
            if bit:
                # 1
                cycle = []
                for i in range(n):
                    u, v, graph_key = keys[i]
                    if not verify_commitment(1, graph_boxes[(u, v)], graph_key):
                        return False
                    next_u, next_v, _ = keys[(i + 1) % n]
                    intersection = set((u, v)).intersection(set((next_u, next_v)))
                    if not len(intersection) == 1:
                        return False
                    cycle.append(intersection.pop())
                # verify if cycle is hamiltonian
                if not len(set(cycle)) == n:
                    return False
            else:
                # 0
                permutation = []
                for i in range(n):
                    graph_perm, graph_key = keys[i]
                    permutation.append(graph_perm)
                    # verify permutation
                    if not verify_commitment(graph_perm, perm_boxes[i], graph_key):
                        return False
                inv_permutation = inv(permutation)
                index = n
                for i in range(n):
                    for j in range(i+1, n):
                        graph_key = keys[index]
                        # verify graph
                        if not verify_commitment(
                            key.public_key[inv_permutation[i], inv_permutation[j]],
                            graph_boxes[(i, j)], graph_key):
                            return False
                        index += 1
    except:
        return False
    return True

def get_bit(bytearray, n):
    byte = n // 8
    shift = n % 8
    return (bytearray[byte] & (1 << shift)) >> shift

def inv(perm):
    inverse = [0] * len(perm)
    for i, p in enumerate(perm):
        inverse[p] = i
    return inverse

def generate_perm(n):
    permutation = list(range(n))
    random.shuffle(permutation)
    return permutation
