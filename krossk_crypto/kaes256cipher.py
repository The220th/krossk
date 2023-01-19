# -*- coding: utf-8 -*-

# taken from here: https://github.com/The220th/py_AES256_cbc_implementation

import sys
import random
import os
import hashlib
import base64
from . import AES256CBC

def utf8_to_bytes(s: str) -> bytes:
    return s.encode("utf-8")

def bytes_to_utf8(bs: bytes) -> str:
    return str(bs, "utf-8")

def calc_hash256(x: str or bytes) -> bytes:
    type_x = type(x)
    if(type_x == bytes or type_x == bytearray):
        return hashlib.sha256(x).digest()
    elif(type_x == str):
        return hashlib.sha256( utf8_to_bytes(x) ).digest()
    else:
        raise AttributeError(f"Cannot cal hash of {type(x)}: \"{x}\". ")

def calc_hash256_str(x: str or bytes) -> str:
    type_x = type(x)
    if(type_x == bytes or type_x == bytearray):
        return hashlib.sha256(x).hexdigest()
    elif(type_x == str):
        return hashlib.sha256( utf8_to_bytes(x) ).hexdigest()
    else:
        raise AttributeError(f"Cannot cal hash of {type(x)}: \"{x}\". ")

def get_random_unicode(lenght):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    S = ''.join(random.choices(letters, k=lenght))
    return S

def get_urandom_bytes(n: int):
    return os.urandom(n)
    # return random.randbytes(n)

class kaes256CBC():

    def __init__(self, key: str or bytes):
        if(len(key) == 0):
            raise ValueError(f"Key is empty: \"{key}\"")
        self.__key = calc_hash256(key)
        self.__bs = 64        # 16*4. if changed, change __salt and __unsalt, __many_salt and __many_unsalt
        self.__bs_salted = 80 # 16*5. if changed, change __salt and __unsalt, __many_salt and __many_unsalt
        self.__READ_bs_count = 15
        self.__info_block_size = 16
        self.__iv_size = 16
        self.__aes = AES256CBC()
    
    def encrypt_msg(self, msg: str) -> str:
        de = utf8_to_bytes(msg)

        en = self._encrypt_bytes(de)

        return base64.b64encode(en).decode("ascii")

    def decrypt_msg(self, en_msg: str) -> str:
        en = base64.b64decode(en_msg.encode("ascii"))
        
        de = self._decrypt_bytes(en)

        return bytes_to_utf8(de)

    def encrypt_file(self, de_src: str, en_dest: str) -> None:
        if(os.path.isfile(de_src) == False):
            raise ValueError(f"{de_src} is not file")
        de_src_abs = os.path.abspath(de_src)
        en_dest_abs = os.path.abspath(en_dest)
        i, N = 0, os.path.getsize(de_src_abs)
        if(N <= 0):
            ex = RuntimeError(f"File \"{de_src_abs}\" is empty. ")
            print(ex, file=sys.stderr)
            raise ex

        BUFF_SIZE = self.__READ_bs_count * self.__bs
        with open(de_src_abs, "rb") as fd_in, open(en_dest_abs, "wb") as fd_out:
            while(i < N):
                buff = fd_in.read(BUFF_SIZE)
                i += BUFF_SIZE
                # print(f"encrypt_file {de_src}: Readed: {len(buff)} bytes")
                out = self._encrypt_bytes(buff)
                fd_out.write(out)
                # print(f"encrypt_file {de_src}: Writed: {len(out)} bytes")
            fd_out.flush()

    def decrypt_file(self, en_src: str, de_dest: str) -> None:
        if(os.path.isfile(en_src) == False):
            raise ValueError(f"{en_src} is not file")
        en_src_abs = os.path.abspath(en_src)
        de_dest_abs = os.path.abspath(de_dest)
        i, N = 0, os.path.getsize(en_src_abs)
        if(N <= 0):
            ex = RuntimeError(f"File \"{en_src_abs}\" is empty. ")
            print(ex, file=sys.stderr)
            raise ex

        BUFF_SIZE = self.__iv_size + self.__info_block_size + self.__READ_bs_count * self.__bs_salted

        #if(N % self.__bs_salted != self.__info_block_size):
        #    ex = RuntimeError(f"File \"{en_src_abs}\" was not encrypted by this cipher. ")
        #    print(ex, file=sys.stderr)
        #    raise ex

        with open(en_src_abs, "rb") as fd_in, open(de_dest_abs, "wb") as fd_out:
            while(i < N):
                buff = fd_in.read(BUFF_SIZE)
                i += BUFF_SIZE
                # print(f"decrypt_file {en_src}: Readed: {len(buff)} bytes")
                out = self._decrypt_bytes(buff)
                fd_out.write(out)
                # print(f"decrypt_file {en_src}: Writed: {len(out)} bytes")
            fd_out.flush()

    def _encrypt_bytes(self, x: bytes) -> bytes:
        de = x

        _hash = calc_hash256(de)[:12]
        pad = self.__calc_pad(de, self.__bs)
        info_block = self.__form_info_block(pad, _hash)
        # print(f"_encrypt_bytes: hash={self.bytes_to_str(_hash)}, pad={pad}")

        de_pad = self.__pad(de, self.__bs)

        de_pad_salted = self.__many_salt(de_pad)

        iv = get_urandom_bytes(self.__iv_size)
        en = self.__aes.EncryptCBC(info_block + de_pad_salted, self.__key, iv)

        return iv + en

    def _decrypt_bytes(self, x: bytes) -> bytes:
        iv, en = x[:self.__iv_size], x[self.__iv_size:]
        
        de_pad_salted = self.__aes.DecryptCBC(en, self.__key, iv)

        info_block, de_pad_salted = de_pad_salted[:self.__info_block_size], de_pad_salted[self.__info_block_size:]
        pad, _hash = self.__get_from_info_block(info_block)

        de_pad = self.__many_unsalt(de_pad_salted)

        de = self.__unpad(de_pad, pad)

        de_hash = calc_hash256(de)[:12]
        # print(f"_decrypt_bytes: hash={self.bytes_to_str(de_hash)}, getted={self.bytes_to_str(_hash)}, getted_pad={pad}")
        if(de_hash != _hash):
            ex = RuntimeError(f"Hashes do not match. ")
            print(ex, file=sys.stderr)
            raise ex

        return de

    def bytes_to_str(self, bs: bytes) -> bytes:
        return self.__aes.printHexArray_str(bs)

    def __form_info_block(self, pad: int, _hash: bytes) -> bytes:
        info_block = bytearray(get_urandom_bytes(self.__info_block_size))
        info_block[3] = pad
        info_block[0], info_block[1], info_block[2], info_block[4]    = _hash[0], _hash[1], _hash[2], _hash[3]
        info_block[5], info_block[6], info_block[7], info_block[8]    = _hash[4], _hash[5], _hash[6], _hash[7]
        info_block[9], info_block[10], info_block[11], info_block[12] = _hash[8], _hash[9], _hash[10], _hash[11]
        return bytes(info_block)

    def __get_from_info_block(self, info_block: bytes) -> tuple:
        """return: (3: pad, 0,1,2,4,5,6,7,8,9,10,11,12: _hash, 13,14,15: not used)"""
        pad = info_block[3]
        _hash = bytearray(12)
        _hash[0], _hash[1], _hash[2], _hash[3]   = info_block[0], info_block[1], info_block[2], info_block[4]
        _hash[4], _hash[5], _hash[6], _hash[7]   = info_block[5], info_block[6], info_block[7], info_block[8]
        _hash[8], _hash[9], _hash[10], _hash[11] = info_block[9], info_block[10], info_block[11], info_block[12]
        return (pad, _hash)

    def __many_salt(self, x: bytes) -> bytes:
        bs = self.__bs
        bs_salted = self.__bs_salted
        len_x = len(x)
        if(len_x == 0 or len_x % bs != 0):
            ex = ValueError(f"__many_salt: lenght of x must devided {bs}, but len = {len_x}")
            print(ex, file=sys.stderr)
            raise ex
        count = len_x // bs
        x_salted = bytearray(bs_salted*count)
        for i in range(count):
            salt_block = self.__salt(x[i*bs:(i+1)*bs])
            for j in range(bs_salted):
                x_salted[i*bs_salted + j] = salt_block[j]
        return bytes(x_salted)

    def __salt(self, x: bytes) -> bytes:
        # every fifth byte insert random stuff
        bs = self.__bs
        if(bs != len(x)):
            ex = ValueError(f"__salt: lenght of x must be {bs}, but len = {len(x)}")
            print(ex, file=sys.stderr)
            raise ex
        bs_salted = self.__bs_salted
        x_salted = bytearray(bs_salted)
        salt = get_urandom_bytes(16)
        j, s = 0, 0
        for i in range(bs_salted):
            if(i % 5 == 0):
                x_salted[i] = salt[s]
                s-=-1
            else:
                x_salted[i] = x[j]
                j+=1
        return bytes(x_salted)

    def __many_unsalt(self, x: bytes) -> bytes:
        bs_salted = self.__bs_salted
        bs = self.__bs
        len_x = len(x)
        if(len_x == 0 or len_x % bs_salted != 0):
            ex = ValueError(f"__many_salt: lenght of x must devided {bs_salted}, but len = {len_x}")
            print(ex, file=sys.stderr)
            raise ex
        count = len_x // bs_salted
        x_unsalted = bytearray(bs*count)
        for i in range(count):
            unsalt_block = self.__unsalt(x[i*bs_salted:(i+1)*bs_salted])
            for j in range(bs):
                x_unsalted[i*bs + j] = unsalt_block[j]
        return bytes(x_unsalted)

    def __unsalt(self, x: bytes) -> bytes:
        # every fifth byte remove
        bs_salted = self.__bs_salted
        if(bs_salted != len(x)):
            ex = ValueError(f"__unsalt: lenght of x must be {bs_salted}, but len = {len(x)}")
            print(ex, file=sys.stderr)
            raise ex
        bs = self.__bs
        x_unsalted = bytearray(bs)
        i = 0
        for j in range(bs_salted):
            if(j % 5 != 0):
                x_unsalted[i] = x[j]
                i+=1
        return bytes(x_unsalted)

    @staticmethod
    def __calc_pad(x: bytes, bs: int) -> int:
        count = (bs - len(x) % bs) % bs
        return count

    @staticmethod
    def __pad(x: bytes, bs: int) -> bytes:
        count = (bs - len(x) % bs) % bs
        shi = count.to_bytes(1, "big")
        return x + shi*count
    
    @staticmethod
    def __unpad(x: bytes, user_count: int = None) -> bytes:
        if(user_count == None):
            len_bs = len(x)
            last = x[len_bs-1] # last is int?
            #count = int.from_bytes(last, "big")
            count = last
        else:
            count = user_count
        if(count == 0):
            return x
        else:
            return x[:-count]
    
    def _tests(self):
        cipher = kaes256CBC("key")
        #for i in range(1000):
        for i in range(0):
            bs = get_urandom_bytes(random.randint(1, 700000))
            #bs = get_urandom_bytes(random.randint(1, 100))
            #bs = b'\x00'*random.randint(0, 17)
            #bs = b'\x01'*random.randint(0, 17)
            #bs = b'\xff'*random.randint(0, 17)
            bs_pad = cipher.__pad(bs, cipher.__bs)
            if(len(bs_pad) % cipher.__bs != 0):
                print(f"({i+1}) error __pad: ")
                print(f"Before: {cipher.bytes_to_str(bs)}\nAfter: {cipher.bytes_to_str(bs_pad)}")
                exit()

            bs_pad_salt = b''
            for i in range(0, len(bs_pad), cipher.__bs):
                bs_pad_salt += cipher.__salt(bs_pad[i:i+cipher.__bs])
            if(len(bs_pad_salt) % cipher.__bs_salted != 0):
                print(f"({i+1}) error __salt: ")
                print(f"src: {cipher.bytes_to_str(bs_pad)}\nsalted: {cipher.bytes_to_str(bs_pad_salt)}")
                exit()

            bs_pad_unsalt = b''
            for i in range(0, len(bs_pad_salt), cipher.__bs_salted):
                bs_pad_unsalt += cipher.__unsalt(bs_pad_salt[i:i+cipher.__bs_salted])
            if(len(bs_pad_unsalt) % cipher.__bs != 0):
                print(f"({i+1}) error __unsalt len: ")
                print(f"src: {cipher.bytes_to_str(bs_pad)}\nunsalted: {cipher.bytes_to_str(bs_pad_unsalt)}")
                exit()
            if(bs_pad_unsalt != bs_pad):
                print(f"({i+1}) error __unsalt dif: ")
                print(f"bs_pad: {cipher.bytes_to_str(bs_pad)}\nsalted: {cipher.bytes_to_str(bs_pad_salt)}\nunsalted: {cipher.bytes_to_str(bs_pad_unsalt)}")
                exit()
            
            bs_pad_salt2 = cipher.__many_salt(bs_pad)
            bs_pad_unsalt2 = cipher.__many_unsalt(bs_pad_salt)
            if(len(bs_pad_salt2) % cipher.__bs_salted != 0 or len(bs_pad_unsalt) % cipher.__bs != 0):
                print(f"({i+1}) error __many_salt/unsalt len: ")
                print(f"bs_pad: {cipher.bytes_to_str(bs_pad)}\nsalted: {cipher.bytes_to_str(bs_pad_salt2)}\nunsalted: {cipher.bytes_to_str(bs_pad_unsalt2)}")
                exit()

            if(bs_pad != bs_pad_unsalt2):
                print(f"({i+1}) error __many_salt/unsalt dif: ")
                print(f"bs_pad: {cipher.bytes_to_str(bs_pad)}\nsalted: {cipher.bytes_to_str(bs_pad_salt2)}\nunsalted: {cipher.bytes_to_str(bs_pad_unsalt2)}")
                exit()

            bs_unpad = cipher.__unpad(bs_pad_unsalt)
            if(bs != bs_unpad):
                print(f"({i+1}) error __unpad: ")
                print(f"src: {cipher.bytes_to_str(bs)}\nunpad: {cipher.bytes_to_str(bs_unpad)}")
                exit()

        for i in range(10):
            key = get_random_unicode(random.randint(1, 300))
            aes = kaes256CBC(key)
            for i in range(100):
                src = get_random_unicode(random.randint(1, 15000))
                en1 = aes.encrypt_msg(src)
                en2 = aes.encrypt_msg(src)
                de1 = aes.decrypt_msg(en1)
                de2 = aes.decrypt_msg(en2)

                aes2 = kaes256CBC(key)
                en3 = aes.encrypt_msg(src)
                de3 = aes.decrypt_msg(en3)
                if(src != de1 or src != de2 or src != de3):
                    print(f"({i+1}) error encrypt/decrypt: ")
                    exit()

        for i in range(10):
            key = get_random_unicode(random.randint(1, 300))
            aes = kaes256CBC(key)
            src_path = "src_file"
            en_path1, de_path1 = "en_file1", "de_file1"
            en_path2, de_path2 = "en_file2", "de_file2"
            en_path3, de_path3 = "en_file3", "de_file3"
            for i in range(100):
                with open(src_path, "wb") as fd:
                    fd.write(random.randbytes(random.randint(1, 4096*5)))
                aes.encrypt_file(src_path, en_path1)
                aes.decrypt_file(en_path1, de_path1)
                aes.encrypt_file(src_path, en_path2)
                aes.decrypt_file(en_path2, de_path2)

                aes2 = kaes256CBC(key)
                en3 = aes.encrypt_file(src_path, en_path3)
                de3 = aes.decrypt_file(en_path3, de_path3)
                with open(src_path, "rb") as fd0, open(de_path1, "rb") as fd1, open(de_path2, "rb") as fd2, open(de_path3, "rb") as fd3: 
                    src, de1, de2, de3 = fd0.read(), fd1.read(), fd2.read(), fd3.read()
                    if(src != de1 or src != de2 or src != de3):
                        print(f"({i+1}) error file encrypt/decrypt: ")
                        print(f"size: src={len(src)}, de1={len(de1)}, de2={len(de2)}, de3={len(de3)}")
                        print(f"src={cipher.bytes_to_str(src)}\nde1={cipher.bytes_to_str(de1)}\nde2={cipher.bytes_to_str(de2)}\nde3={cipher.bytes_to_str(de3)}")
                        exit()
                
                os.unlink(src_path), os.unlink(en_path1), os.unlink(de_path1), os.unlink(en_path2), os.unlink(de_path2), os.unlink(en_path3), os.unlink(de_path3)

        print("All is ok")

if __name__ == '__main__':
    cipher = kaes256CBC("key")
    cipher._tests()
