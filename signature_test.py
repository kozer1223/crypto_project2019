#!/usr/bin/env python3
from modules.signature import sign, verify_sign
from modules.sparsegraph import SparseGraph
from modules.hamiltoniankey import HamiltonianKey
from modules.genkey import generate_key

n = 64
key = generate_key(n)
m = 'hello kolokwium'

signature = sign(m, key)

print(verify_sign(m, key, signature))
print(verify_sign(m + '!', key, signature))
