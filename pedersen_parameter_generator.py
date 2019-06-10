#!/usr/bin/env python3
from Crypto.Util import number
from modules.field import Field

def gen_prime(bits):
    return number.getPrime(bits)

def gen_number(N):
    return number.getRandomRange(2, N)

def gen_generator(F):
    g = F(gen_number(F.modulus()))
    while not g.is_generator():
        g = F(gen_number(F.modulus()))
    return g

bits = 64

p = gen_prime(bits)
print('p:', p)

F = Field(p)

g = gen_generator(F)
print('g:', g)

h = gen_generator(F)
while g == h:
    h = gen_generator(F)
print('h:', h)
