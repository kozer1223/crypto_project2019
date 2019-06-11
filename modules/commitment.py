from .field import Field
from Crypto.Util import number

# parameters
p = 18251104677649902343
Fp = Field(p)
g = Fp(10907332073243075320)
h = Fp(12202716421975369760)

def commit(m):
    r = number.getRandomRange(1, p-1)
    c = g ** m * h ** r

    return (c, r)

def verify_commitment(m, c, r):
    try:
        c.val
    except:
        c = Fp(c)
    return g ** m * h ** r == c
