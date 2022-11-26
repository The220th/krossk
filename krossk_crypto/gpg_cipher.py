# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import re

from . import ICipher


def exe(command : str, debug : bool = True) -> tuple:
    if(debug):
        print(f"> {command}")

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.stdout.read().decode("utf-8")
    err = process.stderr.read().decode("utf-8")
    errcode = process.returncode
    return (out, err, errcode)

def print_gpg_error(comm_out: tuple):
    print("\n-----GPG ERROR-----")
    print(f"stdout: \n{comm_out[0]}")
    print(f"stderr: \n{comm_out[1]}")
    print(f"return code: {comm_out[2]}")
    print("-------------------\n")

class gpg_cipher(ICipher):

    def __init__(self):
        #super().__init__()
        self.__cenz = "***"

    def encrypt_msg(self, msg: str) -> str:
        command = f"echo -n \"{msg}\" | gpg --batch --yes --cipher-algo AES256 --armor --symmetric -"
        command_out = f"echo -n \"{self.__cenz}\" | gpg --batch --yes --cipher-algo AES256 --armor --symmetric -"
        print(f"> {command_out}")

        com_out = exe(command, False)
        if(com_out[0].find("BEGIN PGP MESSAGE") != -1):
            res = com_out[0]
            res = re.match("-----BEGIN PGP MESSAGE-----(.+)-----END PGP MESSAGE-----", res.replace("\n", ""))[1]
        else:
            print_gpg_error(com_out)
            res = "ERORR! CHECK TERMINAL"
        return res


    def decrypt_msg(self, en_msg: str) -> str:
        command = f"echo -ne \"-----BEGIN PGP MESSAGE-----\\n{en_msg}\\n-----END PGP MESSAGE-----\\n\" | gpg --decrypt -"
        command_out = f"echo -ne \"-----BEGIN PGP MESSAGE-----\\n{self.__cenz}\\n-----END PGP MESSAGE-----\\n\" | gpg --decrypt -"
        print(f"> {command_out}")

        com_out = exe(command, False)
        if(com_out[1].find("encrypted with 1 passphrase") != -1):
            res = com_out[0]
        else:
            print_gpg_error(com_out)
            res = "ERORR! CHECK TERMINAL"
        return res

    def encrypt_file(self, de_src: str, en_src: str) -> None:
        raise Exception("NotImplementedException")

    def decrypt_file(self, en_src: str, de_src: str) -> None:
        raise Exception("NotImplementedException")



















