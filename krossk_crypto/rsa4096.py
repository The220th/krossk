# -*- coding: utf-8 -*-

import random
import sys

from . import Base64, bytes_to_int, int_to_bytes

def getNum(n: int) -> int:
    '''get n-bit number'''
    return random.randrange(2**(n-1) + 1, 2**n - 1)

def getNumRange(a: int, b: int) -> int:
    '''get n-bit number [a, b]'''
    return random.randrange(a, b+1)

def getPrime(n: int) -> int:
    '''get n-bit prime number'''
    k = 300
    min_rounds = 30
    while(True):
        res = getNum(n)
        if(MillerRabinTest(res, min_rounds) == True):
            break
    if(MillerRabinTest(res, k) == False):
        res = getPrime(n)
    return res

def MillerRabinTest(n: int, rounds: int) -> int:
    '''True if n probably prime'''
    n_dec = n-1
    if(n == 2 or n == 3):
        return True
    if(n < 2 or n % 2 == 0):
        return False

    t = n - 1
    s = 0
    while(t % 2 == 0):
        t = t // 2
        s += 1

    for i in range(0, rounds):
        a = getNumRange(2, n-2)

        x = pow(a, t, n)

        if(x == 1 or x == n_dec):
            continue

        for r in range(1, s):
            x = pow(x, 2, n)
            if(x == 1):
                return False

            if(x == n_dec):
                break

        if(x != n_dec):
            return False

    return True

def getSophieGermainNum(n: int) -> tuple:
    '''Get n-bit Sophie GermainNum (p, 2*p+1)'''
    k = 300
    min_rounds = 30
    while(True):
        res = getNum(n)
        res2 = res*2 + 1
        if(MillerRabinTest(res, min_rounds) == True and MillerRabinTest(res2, min_rounds) == True):
            break
    if( (MillerRabinTest(res, k) == True and MillerRabinTest(res2, k) == True) == False):
        return getSophieGermainNum(n)
    return (res, res2)

def extendedGCD(a, b) -> tuple:
    '''
    Расширенный алгоритм Евклида:
    a*x + b*y = gcd(a, b)
    return[0]=gcd, return[1]=x, return[2]=y
    '''
    if(b == 0):
        return (a, 1, 0)

    gcd, x1, y1 = extendedGCD(b, a % b)
    x = y1
    y = x1 - (a // b)*y1

    return (gcd, x, y)

def inverse_multiplicative(a, m):
    '''
    Поиск обратного мультипликативного
    a*x = 1 mod(m)
    return x = a^-1
        or
    return None, если нет решения
    '''
    # a*x = 1 mod(m) <==> a*x + m*y = gcd(a, m)
    res = extendedGCD(a, m)
    if(res[0] != 1):
        return None
    else:
        return res[1]

def getPrime_pycrypto(n: int):
    '''get n-bit prime number using pycrypto'''
    from Crypto.Util import number as nbgen
    return nbgen.getPrime(n)

def RSA4096_encrypt(pub_key: str, m: int) -> int:
    b64 = Base64()
    e_str, n_str = pub_key.split("_")
    e = bytes_to_int(b64.decode(e_str))
    ne = bytes_to_int(b64.decode(n_str))
    if(ne > m):
        return pow(m, e, ne)
    return None

class RSA4096:

    def __init__(self):
        prev_recursive_depth = sys.getrecursionlimit()
        sys.setrecursionlimit(4096*4)

        p = getPrime(2048)
        q = getPrime(2048)
        _n = p*q
        p = p - 1
        q = q - 1
        phi = p * q
        while(True):
            _e = getNumRange(getNum(1024), phi-1)
            _d = inverse_multiplicative(_e, phi)
            if( (_d == None or _d.bit_length() < 1024 ) == False):
                break

        self.__pub_key = (_e, _n)
        self.__privKey = (_d, _n)

        sys.setrecursionlimit(prev_recursive_depth)

    def get_pub_key(self) -> tuple:
        '''(e, n)'''
        # return self.__pub_key
        b64 = Base64()
        e_str = b64.encode(int_to_bytes(self.__pub_key[0]))
        n_str = b64.encode(int_to_bytes(self.__pub_key[1]))
        return e_str + "_" + n_str

    def encrypt(self, m: int) -> int:
        e = self.__pub_key[0]
        ne = self.__pub_key[1]
        if(ne > m):
            return pow(m, e, ne)
        return None

    def decrypt(self, m: int) -> int:
        d = self.__privKey[0]
        nd = self.__privKey[1]
        return pow(m, d, nd)

























