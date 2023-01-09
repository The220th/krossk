# -*- coding: utf-8 -*-


import os
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from . import ICipher


class AES256CBC_Cipher(object):
	# https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

    def __init__(self, key: str):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode("utf-8")).digest()

    def encrypt(self, raw : str) -> str:
        raw = base64.b64encode(raw.encode("utf-8")).decode("ascii")

        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        enmsg = base64.b64encode(iv + cipher.encrypt(raw.encode()))
        return enmsg.decode("ascii")

    def decrypt(self, enc : str) -> str:
        enc = enc.encode("ascii")
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        kokoko = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")
        res = base64.b64decode(kokoko.encode("ascii")).decode("utf-8")
        return res

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]



class pycrypto_cipher(ICipher):

    def __init__(self, pswd: str):
        #super().__init__()
        self.__cipher = AES256CBC_Cipher(pswd)
        self.__BUFF_SIZE = 256*1024 # 262144 bytes = 256 KB
        #self.__BUFF_SIZE_EN = 466072 # Сколько байт будет зашифрованный (выходной) блок, если незашифрованный (входной) будет self.__BUFF_SIZE байт
        #self.__BUFF_SIZE = 10
        self.__BUFF_SIZE_EN = self.__get_encrypted_block_size(self.__BUFF_SIZE)
        #print(f"DE={self.__BUFF_SIZE}, EN={self.__BUFF_SIZE_EN}")

    def __get_encrypted_block_size(self, de_block_size: int) -> int:
        # TODO: redo
        buff_cipher = self.__cipher = AES256CBC_Cipher("12345")
        return len(buff_cipher.encrypt("1"*de_block_size))

    def encrypt_msg(self, msg: str) -> str:
        return self.__cipher.encrypt(msg)

    def decrypt_msg(self, en_msg: str) -> str:
        return self.__cipher.decrypt(en_msg)

    def encrypt_file(self, de_src: str, en_src: str) -> None:
        if(os.path.isfile(de_src) == False):
            raise RuntimeError(f"{de_src} is not file")
        de_src_abs = os.path.abspath(de_src)
        en_src_abs = os.path.abspath(en_src)

        i, N = 0, os.path.getsize(de_src_abs)
        if(N <= 0):
            err_msg = f"File \"{de_src_abs}\" is empty. "
            print(err_msg)
            raise RuntimeError(err_msg)
        with open(de_src_abs, "r", encoding="ascii") as fd_in, open(en_src_abs, "w", encoding="ascii") as fd_out:
            while(i < N):
                block = fd_in.read(self.__BUFF_SIZE)
                i += self.__BUFF_SIZE
                block_en = self.__cipher.encrypt(block)
                # print(f"len_DO = {len(block)}, len_nOCJlE = {len(block_en)}")
                fd_out.write(block_en)

    def decrypt_file(self, en_src: str, de_src: str) -> None:
        if(os.path.isfile(en_src) == False):
            raise RuntimeError(f"{en_src} is not file")
        en_src_abs = os.path.abspath(en_src)
        de_src_abs = os.path.abspath(de_src)

        i, N = 0, os.path.getsize(en_src_abs)
        if(N <= 0):
            err_msg = f"File \"{en_src_abs}\" is empty. "
            print(err_msg)
            raise RuntimeError(err_msg)
        with open(en_src_abs, "r", encoding="ascii") as fd_in, open(de_src_abs, "w", encoding="ascii") as fd_out:
            while(i < N):
                block = fd_in.read(self.__BUFF_SIZE_EN)
                i += self.__BUFF_SIZE_EN
                block_de = self.__cipher.decrypt(block)
                # print(f"len_DO = {len(block)}, len_nOCJlE = {len(block_de)}")
                fd_out.write(block_de)


















