import numpy

DEFAULT_N = 4330967
DEFAULT_T = 4318800

def coprime(i, t):
    return numpy.gcd(i, t) == 1

class PublicKey:
    def __init__(self, n, t):
        self.n = n
        self.t = t

    def get(self):
        for i in range(2, self.t):
            if coprime(i, self.t):
                return i
            

class PrivateKey:
    def __init__(self, e: PublicKey):
        self.e = e
        self.n = e.n
        self.t = e.t
        self.s = self.create_key()

    def create_key(self):
        e = self.e.get()
        d = e
        while True:
            d += 1
            if (e * d) % self.t == 1:
                return d
            


class KeyPair:
    def __init__(self, n = DEFAULT_N, t = DEFAULT_T):
        self.e = PublicKey(n, t)
        self.d = PrivateKey(self.e)

    def encrypt(self, msg):
        c = pow(msg, self.e.get()) % self.e.n
        return c
    
    def decrypt(self, c):
        m = pow(c, self.d.s) % self.e.n
        return m
    

