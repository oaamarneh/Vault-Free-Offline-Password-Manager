#!/usr/bin/python
from Crypto.Cipher import AES

import hashlib


# Hashes 1000 times using SHA256
def sha256_hash_1000(password):
    hashed_password = hashlib.sha256(str.encode(password)).hexdigest()
    for _ in range(999):
        hashed_password = hashlib.sha256(str.encode(hashed_password)).hexdigest()
    return hashed_password


# Hashes 500 times using SHA256
def sha256_hash_500(password):
    hashed_password = hashlib.sha256(str.encode(password)).hexdigest()
    for _ in range(499):
        hashed_password = hashlib.sha256(str.encode(hashed_password)).hexdigest()
    return hashed_password


# Hashes 1000 times using MD5
def md5_hash_1000(password):
    hashed_password = hashlib.md5(str.encode(password)).hexdigest()
    for _ in range(1000):
        hashed_password = hashlib.md5(str.encode(hashed_password)).hexdigest()
    return hashed_password


# Encrypts using AES
def aes_encrypt(password, md5_hash):
    padded_password = pad_password(password)
    key = get_aes_key(md5_hash).encode()
    mode = AES.MODE_CBC
    iv = get_aes_iv(md5_hash).encode()
    encryptor = AES.new(key, mode, iv)
    encrypted_password = encryptor.encrypt(padded_password.encode())
    return encrypted_password


# Decrypts AES
def aes_decrypt(encrypted_password, md5_hash):
    key = get_aes_key(md5_hash).encode()
    mode = AES.MODE_CBC
    iv = get_aes_iv(md5_hash).encode()
    encryptor = AES.new(key, mode, iv)
    padded_plain_text_password = encryptor.decrypt(encrypted_password).decode()
    plain_text_password = unpad_password(padded_plain_text_password)
    return plain_text_password


# Returns AES key
def get_aes_key(md5_hash):
    key = md5_hash[0:16]
    return key


# Returns AES initialization vector
def get_aes_iv(md5_hash):
    iv = md5_hash[16:]
    return iv


# Pads password to required length
def pad_password(password):
    while len(password) % 16 != 0:
        password += "="
    padded_password = password
    return padded_password


# Unpads password to the original form
def unpad_password(password):
    while password[-1] == "=":
        password = password[:-1]
    unpadded_password = password
    return unpadded_password