import random
import hashlib

s_box =     {0:0xE, 1:0x4, 2:0xD, 3:0x1, 4:0x2, 5:0xF, 6:0xB, 7:0x8, 8:0x3, 9:0xA, 0xA:0x6, 0xB:0xC, 0xC:0x5, 0xD:0x9, 0xE:0x0, 0xF:0x7} #key:value
s_box_inv = {0xE:0, 0x4:1, 0xD:2, 0x1:3, 0x2:4, 0xF:5, 0xB:6, 0x8:7, 0x3:8, 0xA:9, 0x6:0xA, 0xC:0xB, 0x5:0xC, 0x9:0xD, 0x0:0xE, 0x7:0xF}

pi_p =     {0:0, 1:4, 2:8, 3:12, 4:1, 5:5, 6:9, 7:13, 8:2, 9:6, 10:10, 11:14, 12:3, 13:7, 14:11, 15:15} # permutation
pi_p_inv =  {0:0, 4:1, 8:2, 12:3, 1:4, 5:5, 9:6, 13:7, 2:8, 6:9, 10:10, 14:11, 3:12, 7:13, 11:14, 15:15}

def S_box(state,s_apply):
    sub_states = [state&0x000f, (state&0x00f0)>>4, (state&0x0f00)>>8, (state&0xf000)>>12]
    final_states = sub_states

    for i in range(len(sub_states)):
        final_states[i] = s_apply[sub_states[i]]

    return final_states[0] | final_states[1]<<4 | final_states[2]<<8 | final_states[3]<<12

def permute(state,p):
    final_state = 0      
    for i in range(len(p)):
        if(state & (1 << i)):
            final_state |= (1 << p[i])
    return final_state

def xor_with_k(state,k):
    return state^k 

# Key schedule: independant random round keys.
# We take the sha-hash of a 128-bit 'random' seed and then take the first 80-bits
# of the output as out round keys K1-K5 (Each 16 bits long). (not secure, this is just a demo)
def keyGeneration():
    k = hashlib.sha1( hex(random.getrandbits(128)).encode('utf-8') ).hexdigest()[2:2+20]
    return k

# Encryption Algorithm
def encrypt(plain_text,k):

    state = plain_text

    sub_keys = [ int(s,2) for s in [ k[0:16],k[16:32], k[32:48], k[48:64], k[64:80] ] ]

    for i in range(3):

        # Using the round / sub key to permute the current state
        state = xor_with_k(state,sub_keys[i])

        # Breaking the state into 4 parts and applying s_box to individual parts
        # Here we use the function S_box which performs the above procedure
        state  = S_box(state,s_box)

        # The S_box returns the combined value and hence we can directly apply permutation pi_p on it using the permute function
        state = permute(state,pi_p)

    # Final Round of SPN Cipher
    state = xor_with_k(state,sub_keys[-2])

    state  = S_box(state,s_box)

    state = xor_with_k(state,sub_keys[-1])

    # Finally The Plain Text is Encrypted !!!
    return state

# Decryption Algorithm
def decrypt(cipher_text,k):

    state = cipher_text

    sub_keys = [ int(s,2) for s in [ k[0:16],k[16:32], k[32:48], k[48:64], k[64:80] ] ]

    # Undo the Final Round
    state = xor_with_k(state,sub_keys[-1])

    state  = S_box(state,s_box_inv)

    # Undoing the first 3 rounds
    for i in range(3):

        # Using the round / sub key to permute the current state
        state = xor_with_k(state,sub_keys[3-i])

        # Unpermute the previous state using permutation function with paramter pi_p_inv 
        state = permute(state,pi_p_inv)

        #Apply inverse s-box
        state  = S_box(state,s_box_inv)

    #XOR state with round key 0
    state = xor_with_k(state,sub_keys[0])

    # Finally the cipher text in decrypted !!!
    return state

if __name__ == "__main__":
    
    # Generate a randon key
    # k = keyGeneration()
    k = "00111010100101001010100101001101100101001101011001001101011000111101011000111111"
    x = 0b0010011010110111
    y = encrypt(x,k)
    x_d = decrypt(y,k)
    print(bin(y)[2:])
    if x_d == x:
        print("Yayy!!!")