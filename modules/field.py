from functools import reduce

def Field(n):
    # should check if n is prime, but w/e
    class Field():
        __phi_n = n - 1
        __phi_n_factors = None

        def __init__(self, val):
            self.val = val % n
        @staticmethod
        def modulus():
            return n
        def legendre(self):
            l = (self ** ((n-1)//2)).val
            return l if l != n-1 else -1
        def roots(self):
            # return square roots
            if self.legendre() == 0:
                return [0]
            if self.legendre() == -1:
                return []
            for a in (Field(i) for i in range(2, n)):
                b = a**2 - self
                if b.legendre() == -1:
                    k = CipollaField(n, b)(a, Field(1)) ** ((n + 1) // 2)
                    return [k.x, -k.x]
        def is_generator(self):
            if self.val == 0:
                return False
            # init phi(n) factorization
            if not Field.__phi_n_factors:
                Field.__phi_n_factors = factors(Field.__phi_n)
            for factor in Field.__phi_n_factors:
                if factor != Field.__phi_n and self ** factor == Field(1):
                    return False
            return True
        def __str__(self):
            return str(self.val)
        def __repr__(self):
            return str(self)
        def __eq__(self, other):
            return self.val == other.val
        def __neq__(self, other):
            return self.val != other.val
        def __add__(self, other):
            if isinstance(other, int):
                return Field(self.val + other)
            return Field(self.val + other.val)
        def __sub__(self, other):
            if isinstance(other, int):
                return Field(self.val - other)
            return Field(self.val - other.val)
        def __mul__(self, other):
            if isinstance(other, int):
                return Field(self.val * other)
            return Field(self.val * other.val)
        def __truediv__(self, other):
            if isinstance(other, int):
                return Field(self.val * modinv(other, n))
            return Field(self.val * modinv(other.val, n))
        def __pow__(self, other):
            if isinstance(other, int):
                return Field(pow(self.val, other, n))
            return Field(pow(self.val, other.val, n))
        def __mod__(self, other):
            return Field(self.val % other.val)
        def __neg__(self):
            return Field(n - self.val)
    return Field

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("no inverse")
    else:
        return x % m

def CipollaField(p, b):
    class CipollaField():
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __str__(self):
            return f'({self.x}, {self.y})'
        def __repr__(self):
            return str(self)
        def __add__(self, other):
            return CipollaField(self.x + other.x, self.y + other.y)
        def __mul__(self, other):
            return CipollaField(
                self.x * other.x + self.y * other.y * (b),
                self.x * other.y + self.y * other.x
            )
        def __pow__(self, n):
            if n == 0:
                return CipollaField(Field(p)(1), Field(p)(0))
            a = self
            b = CipollaField(Field(p)(1), Field(p)(0))
            while (n > 1):
                r = n % 2
                n = (n - r) // 2
                if r == 1:
                    b = a * b
                    a = a * a
                else:
                    a = a * a
            return a * b
    return CipollaField

def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
