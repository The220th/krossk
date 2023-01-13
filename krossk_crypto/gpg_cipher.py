# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import re
import hashlib

from . import ICipher

def calc_sha256(s: str) -> str:
    bs = s.encode("utf-8")
    m = hashlib.sha256()
    m.update(bs)
    res = m.hexdigest()
    return res

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

    def __init__(self, key: str):
        '''key_is_file = path_to_key_file'''
        #super().__init__()
        self.__cenz = "***"
        self.key = calc_sha256(key)

    def encrypt_msg(self, msg: str) -> str:
        command = f"echo -n \"{msg}\" | gpg --batch --yes --cipher-algo AES256 --passphrase \"{self.key}\" --armor --symmetric -"
        command_out = f"echo -n \"{self.__cenz}\" | gpg --batch --yes --cipher-algo AES256 --passphrase \"{self.__cenz}\" --armor --symmetric -"
        print(f"> {command_out}")

        com_out = exe(command, False)
        if(com_out[0].find("BEGIN PGP MESSAGE") != -1):
            res = com_out[0]
            res = re.match("-----BEGIN PGP MESSAGE-----(.+)-----END PGP MESSAGE-----", res.replace("\n", ""))[1]
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")
        return res

    def decrypt_msg(self, en_msg: str) -> str:
        command = f"echo -ne \"-----BEGIN PGP MESSAGE-----\\n{en_msg}\\n-----END PGP MESSAGE-----\\n\" | gpg --decrypt --batch --passphrase \"{self.key}\" -"
        command_out = f"echo -ne \"-----BEGIN PGP MESSAGE-----\\n{self.__cenz}\\n-----END PGP MESSAGE-----\\n\" | gpg --decrypt --batch --passphrase \"{self.__cenz}\" -"
        print(f"> {command_out}")

        com_out = exe(command, False)
        if(com_out[1].find("encrypted with 1 passphrase") != -1):
            res = com_out[0]
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")
        if(res == ""):
            raise RuntimeError("GPG ERROR. Invalid key?")
        return res

    def encrypt_file(self, de_src: str, en_src: str) -> None:
        if(os.path.isfile(de_src) == False):
            raise RuntimeError(f"{de_src} is not file")
        de_src_abs = os.path.abspath(de_src)
        en_src_abs = os.path.abspath(en_src)

        command = f"gpg --output {en_src} --batch --yes --cipher-algo AES256 --passphrase \"{self.key}\" --armor --symmetric {de_src_abs}"
        command_out = f"gpg --output {en_src} --batch --yes --cipher-algo AES256 --passphrase \"{self.__cenz}\" --armor --symmetric {de_src_abs}"
        print(f"> {command_out}")

        com_out = exe(command, False)
        if(com_out[0] == ""):
            print("gpg encrypt file: ok")
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")

    def decrypt_file(self, en_src: str, de_src: str) -> None:
        if(os.path.isfile(en_src) == False):
            raise RuntimeError(f"{en_src} is not file")
        en_src_abs = os.path.abspath(en_src)
        de_src_abs = os.path.abspath(de_src)

        command = f"gpg --output {de_src} --decrypt --batch --yes --passphrase \"{self.key}\" {en_src}"
        command_out = f"gpg --output {de_src} --decrypt --batch --yes --passphrase \"{self.__cenz}\" {en_src}"
        print(f"> {command_out}")

        com_out = exe(command, False)
        if(com_out[0] == ""):
            print("gpg decrypt file: ok")
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")
    
    def check_gpg_insystem_exists(self):
        command = "gpg --version"
        com_out = exe(command)
        if(com_out[0].find("gpg (GnuPG)") != -1):
            return True
        else:
            return False
