import random
import hashlib
from DES_parameters import *

def pbox(x,p,n):

    y = 0

    for i in p:
        y <<= 1
        y ^= (x >> (n-i)) & 1
        
    return y

def key_scheduling(k):

    keys = []
    
    x = pbox(k,pc1,64)

    for i in range(16):

        if i in [0, 1, 8, 15]:
            x = pbox(x,rhl1,56)
        else:
            x = pbox(x,rhl2,56)

        keys.append(pbox(x,pc2,56))

    return keys