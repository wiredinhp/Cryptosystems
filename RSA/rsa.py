from rsa_keypair_generation import *

def encrypt(pk, plaintext):

    b, n = pk
    ciphertext = [(ord(x) ** b) % n for x in plaintext]
    #Return the array of bytes
    return ciphertext

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    a, n = pk
    plaintext = [chr((x ** a) % n) for x in ciphertext]
    return ''.join(plaintext)


if __name__ == '__main__':

    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = keypair_generation(p, q)
    print("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(encrypted_msg)
    print("Decrypting message with public key ", public ," . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))