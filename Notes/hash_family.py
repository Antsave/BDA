"""
Author: Sunil Shende

A Universal family of hash functions has the property that for any pair of
keys in the universe of keys (`U`), a hash function drawn uniformly at
random from the family will cause the keys to collide with an expected
probability of 1/m, where m is the table size. It uses a prime number
p > |`U`|.

In the `make_hash` method, we choose a, b to be random integers chosen
uniformly in the ranges 1 <= a <= p-1 and 0 <= b <= p-1.
"""
import numpy as np
import secrets

class UHF:
    """A factory for producing a universal family of hash functions"""

    @staticmethod
    def is_prime(k):
        if k%2==0:
            return False
        for i in range(3, int(np.sqrt(k)), 2):
            if k%i == 0:
                return False
        return True

    def __init__(self, n):
        """Universe size is n"""
        self.n = n
        self.rng = np.random.default_rng()
        if n%2==0:
            m = n+1
        else:
            m = n+2
        while not(UHF.is_prime(m)):
            m = m+2
        self.p = m

    def make_hash(self, m):
        """Return a random hash function

        m: table size
        """
        a = self.rng.integers(1,self.p)
        b = self.rng.integers(0,self.p)
        return lambda k: ((a*k +b) % self.p) % m

def make_string_hash(m:np.uint64 = 2**61 - 1):
    """Return a random hash function for a string

    Uses a default table size == 9th Mersenne prime

    m: table size
    """
    SALT = secrets.token_hex(12)
    P = 521 # a prime larger than 256
    def poly_hash(x):
        x += SALT
        bx = x.encode('utf-8')
        result = 0
        for i in range(len(bx)):
            result = (P*result + bx[i]) % m
        return hex(result)
    return poly_hash
