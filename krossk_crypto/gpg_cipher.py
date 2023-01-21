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

def decode_out(_stdout, _stderr) -> (str, str):
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    try:
        res = (_stdout.decode("utf-8"), _stderr.decode("utf-8"))
    except:
        try:
            res = (_stdout.decode("cp1251"), _stderr.decode("cp1251"))
        except:
            try:
                res = (_stdout.decode("cp866"), _stderr.decode("cp866"))
            except:
                try:
                    res = (_stdout.decode("ascii"), _stderr.decode("ascii"))
                except:
                    res = (_stdout.decode(), _stderr.decode())
    return res

def exe(command: list, stdin_msg: str, debug : bool = True) -> tuple:
    if(debug):
        print(f"> ", end="")
        print(*command)

    proc = subprocess.run(command, capture_output=True, input=stdin_msg.encode("utf-8"))
    
    #return (proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"))
    return decode_out(proc.stdout, proc.stderr)

def print_gpg_error(comm_out: tuple):
    print("\n-----GPG ERROR-----")
    print(f"stdout: \n{comm_out[0]}")
    print(f"stderr: \n{comm_out[1]}")
    #print(f"return code: {comm_out[2]}")
    print("-------------------\n")

class gpg_cipher(ICipher):

    def __init__(self, key: str):
        self.__cenz = "***"
        self.key = calc_sha256(key)

    def encrypt_msg(self, msg: str) -> str:
        command = ["gpg", "--batch", "--yes", "--cipher-algo", "AES256", "--passphrase", f"\"{self.key}\"", "--armor", "--symmetric", "-"]
        command_out = ["gpg", "--batch", "--yes", "--cipher-algo", "AES256", "--passphrase", f"\"{self.__cenz}\"", "--armor", "--symmetric", "-"]
        print(f"> ", end="")
        print(*command_out)

        com_out = exe(command, msg, False)
        if(com_out[0].find("BEGIN PGP MESSAGE") != -1):
            res = com_out[0]
            res = re.match("-----BEGIN PGP MESSAGE-----(.+)-----END PGP MESSAGE-----", res.replace("\n", ""))[1]
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")
        return res

    def decrypt_msg(self, en_msg: str) -> str:
        stdin_msg = f"-----BEGIN PGP MESSAGE-----\n{en_msg}\n-----END PGP MESSAGE-----\n"
        command = ["gpg", "--decrypt", "--batch", "--passphrase", f"\"{self.key}\"", "-"]
        command_out = ["gpg", "--decrypt", "--batch", "--passphrase", f"\"{self.__cenz}\"", "-"]
        print(f"> ", end="")
        print(*command_out)

        com_out = exe(command, stdin_msg, False)
        if(com_out[1].find("encrypted with 1 passphrase") != -1):
            res = com_out[0]
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")
        if(res == ""):
            raise RuntimeError("GPG ERROR. Invalid key?")
        return res

    def encrypt_file(self, de_src: str, en_src: str) -> None: # TODO
        if(os.path.isfile(de_src) == False):
            raise RuntimeError(f"{de_src} is not file")
        de_src_abs = os.path.abspath(de_src)
        en_src_abs = os.path.abspath(en_src)

        command = ["gpg", "--output", f"{en_src}", "--batch", "--yes", "--cipher-algo", "AES256", "--passphrase", f"\"{self.key}\"", "--armor", "--symmetric", f"{de_src_abs}"]
        command_out = ["gpg", "--output", f"{en_src}", "--batch", "--yes", "--cipher-algo", "AES256", "--passphrase", f"\"{self.__cenz}\"", "--armor", "--symmetric", f"{de_src_abs}"]
        print(f"> ", end="")
        print(*command_out)

        com_out = exe(command, "", False)
        if(com_out[0] == ""):
            print("gpg encrypt file: ok")
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key?")

    def decrypt_file(self, en_src: str, de_src: str) -> None: # TODO
        if(os.path.isfile(en_src) == False):
            raise RuntimeError(f"{en_src} is not file")
        en_src_abs = os.path.abspath(en_src)
        de_src_abs = os.path.abspath(de_src)

        command = ["gpg", "--output", f"{de_src}", "--decrypt", "--batch", "--yes", "--passphrase", f"\"{self.key}\"", f"{en_src}"]
        command_out = ["gpg", "--output", f"{de_src}", "--decrypt", "--batch", "--yes", "--passphrase", f"\"{self.__cenz}\"", f"{en_src}"]
        print(f"> ", end="")
        print(*command_out)

        com_out = exe(command, "", False)
        print(com_out)
        if(com_out[1].find("failed") == -1):
            print("gpg decrypt file: ok")
        else:
            print_gpg_error(com_out)
            raise RuntimeError("GPG ERROR. Invalid key or file?")
    
    def check_gpg_insystem_exists(self):
        try:
            com_out = exe(["gpg", "--version"], "")
            #print(com_out)
            if(com_out[0].find("gpg (GnuPG)") != -1):
                return True
            else:
                return False
        except:
            return False
