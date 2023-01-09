# -*- coding: utf-8 -*-


from krossk_crypto import RSA4096

def test_import():
    rsa = RSA4096()
    en_msg = rsa.encrypt(1261251)
    de_msg = rsa.decrypt(en_msg)
    print(de_msg)
