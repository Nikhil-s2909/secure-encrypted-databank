from Crypto.Cipher import Blowfish
import os

BLOCK_SIZE = 8

def pad(data):
    return data + b"\0" * (BLOCK_SIZE - len(data) % BLOCK_SIZE)

def encrypt_file(path, key):
    with open(path, 'rb') as f:
        data = f.read()

    cipher = Blowfish.new(key.encode(), Blowfish.MODE_ECB)
    encrypted = cipher.encrypt(pad(data))

    with open(path, 'wb') as f:
        f.write(encrypted)
