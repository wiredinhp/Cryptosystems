import random
import hashlib
from DES_key_scheduling import *
from DES_parameters import *

def S_boxes(state,s_apply):

    sub_states = []
    for i in range(8):

        temp = 0
        val = 0

        for j in range(6):
            val |= (1<<(6*i+j))

        temp = state & val     
        temp = temp >> (6*i)
        sub_states.append(temp)
    
    # print(sub_states)
    sub_states.reverse()

    final_states = []

    for i in range(8):
        final_states.append(s_apply[i][sub_states[i]])

    final_states.reverse()

    return final_states[0] | final_states[1]<<4 | final_states[2]<<8 | final_states[3]<<12 | final_states[4]<<16 | final_states[5]<<20 | final_states[6]<<24 | final_states[7]<<28

def xor_with_k(state,k):
    return state^k 

def expansion(A):
    return pbox(A,E,32)
    ##
    
def f(A,J):
    # Expanding the 32 bit A to a bitstring of length 48 
    A_e = expansion(A)

    # XOR-ing the expanded value with J
    f_output = xor_with_k(A_e,J)

    # Feeding the resulting value to the S_boxes
    f_output = S_boxes(f_output,s)

    # Permutation done in every round
    f_output = pbox(f_output,p0,32)
    ##
    return f_output

def g(l,r,k):
    
    l_next = r

    r_next = xor_with_k(f(r,k),l)

    return l_next, r_next
    ##

def g_inv(l,r,k):
    
    r_next = l

    l_next = xor_with_k(f(l,k),r)

    return l_next, r_next
    ##

def encrypt(plain_text,k):

    # Applying the initial permutation to the Plain Text
    state = pbox(plain_text,IP,64)

    # Splitting the bitstring in 2 halves
    l_state = (state & (int(("1"*32)+("0"*32),2))) >> 32
    r_state = state & (int("1"*32,2))

    # Applying KSA on the 64 bit key given as input
    sub_keys = key_scheduling(k)
    
    # Performing the 16 rounds
    for i in range(16):

        # Applying the round function g to the current values
        l_state, r_state = g(l_state,r_state,sub_keys[i])

    # Combining the 2 states in reverse order
    state = (r_state<<32) | (l_state)

    # Applying the inverse of initial permutation
    state = pbox(state,IP_inv,64)
    # Finally The Plain Text is Encrypted !!!
    return state

def decrypt(cipher_text,k):
    # Applying the inverse of inverse , i.e the initial permutation to the Plain Text
    state = pbox(cipher_text,IP,64)

    # Splitting the bitstring in 2 halves in reverse manner
    r_state = (state & (int(("1"*32)+("0"*32),2))) >> 32
    l_state = state & (int("1"*32,2))

    # Applying KSA on the 64 bit key given as input
    sub_keys = key_scheduling(k)
    
    # Performing the 16 rounds
    for i in range(16):

        # Applying the round function g to the current values
        l_state, r_state = g_inv(l_state,r_state,sub_keys[15-i])

    # Combining the 2 states in same order
    state = (l_state<<32) | (r_state)

    # Applying the inverse of initial permutation
    state = pbox(state,IP_inv,64)

    # Finally The Cipher Text is Encrypted !!!
    return state
    ##

if __name__ == "__main__":
    
    k = int('AABB09182736CCDD',16)
    plain_text = int('123456ABCD132536',16)
    print(hex(encrypt(plain_text,k))[2:])
    cipher_text = int('C0B7A8D05F3A829C',16)
    print(hex(decrypt(cipher_text,k))[2:])