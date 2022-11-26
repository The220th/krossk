# -*- coding: utf-8 -*-


import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from . import ICipher


class AES256CBC_Cipher(object):
	# https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

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
        kokoko = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
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

    def encrypt_msg(self, msg: str) -> str:
        return self.__cipher.encrypt(msg)

    def decrypt_msg(self, en_msg: str) -> str:
        return self.__cipher.decrypt(en_msg)

    def encrypt_file(self, de_src: str, en_src: str) -> None:
        raise Exception("NotImplementedException")

    def decrypt_file(self, en_src: str, de_src: str) -> None:
        raise Exception("NotImplementedException")



















