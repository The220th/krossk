# -*- coding: utf-8 -*-

import hashlib

import string
import random

def utf8_to_bytes(s: str) -> bytes:
    return s.encode("utf-8")

def bytes_to_utf8(bs: bytes) -> str:
    return str(bs, "utf-8")

def bytes_to_int(b_arr: bytes) -> int:
    return int.from_bytes(b_arr, "big")

def int_to_bytes(a: int, bytesLen: int = None) -> bytes:
    if(bytesLen == None):
        return a.to_bytes((a.bit_length()+7)//8, "big")
    else:
        return a.to_bytes(bytesLen, "big")

def calc_hash(x: bytes or str) -> str:
    if(type(x) == bytes):
        return hashlib.sha256(x).hexdigest()
    elif(type(x) == str):
        return hashlib.sha256( utf8_to_bytes(x) ).hexdigest()
    else:
        raise AttributeError(f"Cannot cal hash of {type(x)}: \"{x}\". ")

def calc_hash_512(x: bytes or str) -> (str, bytes):
    if(type(x) == bytes):
        buff = hashlib.sha512(x)
        return (buff.hexdigest(), buff.digest())
    elif(type(x) == str):
        buff = hashlib.sha512( utf8_to_bytes(x) )
        return (buff.hexdigest(), buff.digest())
    else:
        raise AttributeError(f"Cannot cal hash of {type(x)}: \"{x}\". ")

def calc_hash_file(file_path: str) -> str:
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

class Base64(object):
    # https://gist.github.com/trondhumbor/ce57c0c2816bb45a8fbb
    __author__ = "Tsh"

    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789=/"
    FORBIDDEN_SYM = ":" # "="

    def __chunk(self, data, length):
        return [data[i:i+length] for i in range(0, len(data), length)]

    def encode(self, data):
        override = 0
        if len(data) % 3 != 0:
            override = (len(data) + 3 - len(data) % 3) - len(data)
        data += b"\x00"*override

        threechunks = self.__chunk(data, 3)

        binstring = ""
        for chunk in threechunks:
            for x in chunk:
                binstring += "{:0>8}".format(bin(x)[2:])

        sixchunks = self.__chunk(binstring, 6)

        outstring = ""
        for element in sixchunks:
            outstring += self.CHARS[int(element, 2)]
        
        outstring = outstring[:-override] + self.FORBIDDEN_SYM*override
        return outstring

    def decode(self, data):
        override = data.count(self.FORBIDDEN_SYM)
        data = data.replace(self.FORBIDDEN_SYM, "A")
        
        binstring = ""
        for char in data:
            binstring += "{:0>6b}".format(self.CHARS.index(char))

        eightchunks = self.__chunk(binstring, 8)
        
        outbytes = b""
        for chunk in eightchunks:
            outbytes += bytes([int(chunk, 2)])

        return outbytes[:-override]

def getRandomString(lenght : int = 20) -> str:
    S = ''.join(random.choices(string.ascii_uppercase + string.digits, k=lenght))
    return S

def gen_password() -> str:
    while(True):
        len_i = random.randint(30, 64)
        S = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + ".,!@#$%^&*)(-_+=?/", k=len_i))
        if(check_passphrase_is_strong(S) == True):
            break
    return S

def check_passphrase_is_strong(passphrase: str) -> bool:
    if(len(passphrase) < 8):
        return False
    
    lower, upper, digits, symbols = False, False, False, False

    for c in passphrase:
        if(c in string.ascii_lowercase):
            lower = True
        if(c in string.ascii_uppercase):
            upper = True
        if(c in string.digits):
            digits = True
        if(c in ".,!@#$%^&*)(-_+=?/"):
            symbols = True

    if(False in [lower, upper, digits, symbols]):
        return False

    return True