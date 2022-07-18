import random

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b,a%b)

def is_prime(a):
    if a < 2: return False
    for x in range(2, int(a**0.5) + 1):
        if a % x == 0:
            return False
    return True

def modInverse(a, m):
     
    for x in range(1, m):
        if (((a%m) * (x%m)) % m == 1):
            return x
    return -1

def keypair_generation(p,q):

    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p*q
    phi = (p-1)*(q-1)

    b = random.randrange(1, phi)
    while gcd(b,phi) !=1:
        b = random.randrange(1, phi)
    
    a = modInverse(b,phi)

    return ((b,n), (a,n))
