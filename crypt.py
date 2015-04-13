__author__ = 'team14'

import sys
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES


# Returns randomly generated RSA key object
def create_private_key():
    return RSA.generate(2048)

# Creates new key and places contents in key_file
def make_key(key_file):
    new_key = RSA.generate(2048)
    file_obj = open(key_file, 'wb')
    file_obj.write(new_key.exportKey())
    file_obj.close()


# Encrypts file_to_enc to enc_file using key: key_file
def en_crypt(key_file, file_to_enc, enc_file):
    # Load key from key_file
    file_obj = open(key_file, 'rb')
    file_contents = file_obj.read()
    key_copy = RSA.importKey(file_contents)
    # Use key to encrypt file_to_enc
    file_obj = open(file_to_enc, 'rb')
    file_contents = file_obj.read()
    enc_tuple = key_copy.encrypt(file_contents, 0)
    file_obj = open(enc_file, 'wb')
    file_obj.write(enc_tuple[0])
    file_obj.close()


# Decrypts file_to_dec into dec_file using key: private_key_file
def de_crypt(private_key_file, file_to_dec, dec_file):
    # Load private key from private_key_file
    file_obj = open(private_key_file, 'rb')
    file_contents = file_obj.read()
    key_copy = RSA.importKey(file_contents)
    # Use key to decrypt file_to_dec
    file_obj = open(file_to_dec, 'rb')
    file_contents = file_obj.read()
    dec_tuple = key_copy.decrypt(file_contents)
    file_obj = open(dec_file, 'wb')
    file_obj.write(dec_tuple)
    file_obj.close()


# Returns public key object, capable of encrypting files.
def get_public_key(private_key):
    return private_key.publickey()


# Takes in either public key or private key and encrypts
# file_to_enc and writes the encrypted value onto enc_file
def encrypt_file(key, file_to_enc, enc_file):
    file_obj = open(file_to_enc, 'rb')
    file_contents = file_obj.read()
    enc_tuple = key.encrypt(file_contents, 0)
    file_obj = open(enc_file, 'wb')
    file_obj.write(enc_tuple[0])
    file_obj.close()


# Takes in file_to_dec and writes the decrypted value into dec_file.
# Decryption cannot work with public key.
def decrypt_file(private_key, file_to_dec, dec_file):
    file_obj = open(file_to_dec, 'rb')
    file_contents = file_obj.read()
    dec_tuple = private_key.decrypt(file_contents)
    file_obj = open(dec_file, 'wb')
    file_obj.write(dec_tuple)
    file_obj.close()


# Returns tuple signature of type long, can only sign with private key
def get_signature(private_key, file_to_send):
    file_obj = open(file_to_send, 'rb')
    file_contents = file_obj.read()
    file_obj.close()
    return private_key.sign(file_contents, 0)


# Returns true if signature corresponds with file_received, else false.
# Both public and private keys may be used
def verify_signature(key, signature, file_received):
    file_obj = open(file_received, 'rb')
    file_contents = file_obj.read()
    file_obj.close()
    return key.verify(file_contents, signature)

if __name__ == "__main__":
    if sys.argv[1] == "private":
        make_key(sys.argv[2])
    elif sys.argv[1] == "encrypt":
        en_crypt(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "decrypt":
        de_crypt(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Error: invalid command")