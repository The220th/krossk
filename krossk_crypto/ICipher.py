# -*- coding: utf-8 -*-

class ICipher(object):

    def __init__(self):
        pass

    def encrypt_msg(self, msg: str) -> str:
        raise Exception("NotImplementedException")

    def decrypt_msg(self, en_msg: str) -> str:
        raise Exception("NotImplementedException")

    def encrypt_file(self, de_src: str, en_src: str) -> None:
        raise Exception("NotImplementedException")

    def decrypt_file(self, en_src: str, de_src: str) -> None:
        raise Exception("NotImplementedException")
