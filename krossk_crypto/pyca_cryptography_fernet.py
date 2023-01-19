# -*- coding: utf-8 -*-

from . import utf8_to_bytes, bytes_to_utf8, int_to_bytes, bytes_to_int

from cryptography.fernet import Fernet
import hashlib
import base64
import os

class Pyca_Fernet(object):

    def __init__(self, key: str):
        self.key = base64.urlsafe_b64encode(hashlib.sha256(key.encode("utf-8")).digest())
        self.__f = Fernet(self.key)
        self.__BUFF_SIZE = 256*1024

    def encrypt_msg(self, msg: str) -> str:
        data = utf8_to_bytes(msg)
        en = self.__f.encrypt(data)
        res = base64.b64encode(en).decode("ascii")
        return res

    def decrypt_msg(self, en_msg: str) -> str:
        en = base64.b64decode(en_msg.encode("ascii"))
        de = self.__f.decrypt(en)
        res = bytes_to_utf8(de)
        return res

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

        with open(de_src_abs, "rb") as fd_in, open(en_src_abs, "wb") as fd_out:
            while(i < N):
                block = fd_in.read(self.__BUFF_SIZE)
                i += self.__BUFF_SIZE
                block_en = self.__f.encrypt(block)
                fd_out.write(int_to_bytes(len(block_en), 8) + block_en)
            fd_out.flush()


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

        with open(en_src_abs, "rb") as fd_in, open(de_src_abs, "wb") as fd_out:
            while(i < N):
                block_size = bytes_to_int(fd_in.read(8))
                block = fd_in.read(block_size)
                i += block_size + 8
                block_de = self.__f.decrypt(block)
                fd_out.write(block_de)
            fd_out.flush()
