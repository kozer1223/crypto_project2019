#!/usr/bin/env python3
from modules.signature import sign, verify_sign, write_signature, read_signature
from modules.sparsegraph import SparseGraph
from modules.hamiltoniankey import HamiltonianKey
from modules.genkey import generate_key


n = 64
key = generate_key(n)
m = 'hello kolokwium'

json_sign = write_signature(sign(m, key))
signature = read_signature(json_sign)

print(verify_sign(m, key, signature))
print(verify_sign(m + '!', key, signature))
