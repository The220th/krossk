# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import PasswordWidget, ifMsg
from . import ico_get_file

from krossk_crypto import Pyca_Fernet, gpg_cipher, kaes256CBC, check_passphrase_is_strong

import os
import threading

def thread_func(parent: "QWidget", cipher: "ICipher", ENCRYPT_DECRYPT: bool, path_src: str, path_dest: str):
    try:
        if(ENCRYPT_DECRYPT == False):
            cipher.encrypt_file(path_src, path_dest)
            #ifMsg(None, f"Finished.\n\nFile \"{path_src}\"\n encrypted\n to \"{path_dest}\". ", 2)
            parent.show_msg(f"Finished.\n\nFile \"{path_src}\"\n encrypted\n to \"{path_dest}\". ", 2)
        else:
            cipher.decrypt_file(path_src, path_dest)
            #ifMsg(None, f"Finished.\n\nFile \"{path_src}\"\n decrypted\n to \"{path_dest}\". ", 2)
            parent.show_msg(f"Finished.\n\nFile \"{path_src}\"\n decrypted\n to \"{path_dest}\". ", 2)
    except:
        import traceback
        print(traceback.format_exc())
        parent.show_msg("Cannot encrypt/decrypt file! \nInvalid key or file?", 4)
    parent.set_en_de_Mutex(False)

class FileTransferWidget(QWidget):

    __ciphers_list = ["PyCA Fernet AES128-cbc", "GPG AES256", "GPG default", "kaes256CBC (very slow)"] # порядок не менять! 

    def __init__(self, parent):
        super().__init__(parent)
        self.__xcrypt_button_mutex = False
        self.__last_filename_src = None
        self.__last_filename_dest = None
        self.cipher_mode = None

        self.__grid = QGridLayout()

        self.__pswd = PasswordWidget(self, "Passphrase")

        self.__ciphers_combo = QComboBox(self)
        self.__ciphers_combo.addItems(self.__ciphers_list)
        self.__ciphers_combo.activated[str].connect(self.__ciphers_combo_handler)
        self.__ciphers_combo_prev_index = 0

        self.__file_src_pick = QPushButton(ico_get_file(), "Pick file source", self)
        self.__file_src_pick.clicked.connect(lambda:self.__file_src_pick_handler())

        self.__file_dest_pick = QPushButton(ico_get_file(), "Pick file destination", self)
        self.__file_dest_pick.clicked.connect(lambda:self.__file_dest_pick_handler())

        self.__file_src_text = QLineEdit(self)
        self.__file_src_text.setReadOnly(False)

        self.__file_dest_text = QLineEdit(self)
        self.__file_dest_text.setReadOnly(False)

        self.__encrypt_button = QPushButton("Encrypt", self)
        self.__encrypt_button.clicked.connect(lambda:self.__encrypt_button_handler())

        self.__decrypt_button = QPushButton("Decrypt", self)
        self.__decrypt_button.clicked.connect(lambda:self.__decrypt_button_handler())

        self.__info_msg_label = QLabel("", self)

        buffWidget = QWidget(self)
        buff_grid = QGridLayout()
        buff_grid.addWidget(self.__encrypt_button, 0, 0, 1, 1)
        buff_grid.addWidget(self.__decrypt_button, 0, 1, 1, 1)
        buffWidget.setLayout(buff_grid)

        buffWidget2 = QWidget(self)
        buff_grid2 = QGridLayout()
        buff2_label = QLabel("Select cipher:", self)
        buff2_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        buff_grid2.addWidget(buff2_label, 0, 0, 1, 1)
        buff_grid2.addWidget(self.__ciphers_combo, 0, 1, 1, 1)
        buffWidget2.setLayout(buff_grid2)

        self.__grid.addWidget(self.__pswd, 0, 0, 1, 1)
        self.__grid.addWidget(buffWidget2, 0, 1, 1, 1)
        self.__grid.addWidget(self.__file_src_pick, 1, 0, 1, 1)
        self.__grid.addWidget(self.__file_src_text, 1, 1, 1, 1)
        self.__grid.addWidget(self.__file_dest_pick, 2, 0, 1, 1)
        self.__grid.addWidget(self.__file_dest_text, 2, 1, 1, 1)
        self.__grid.addWidget(self.__info_msg_label, 3, 0, 1, 2)
        self.__grid.addWidget(buffWidget, 4, 0, 1, 2)

        self.__grid.setRowStretch(0, 0)
        self.setLayout(self.__grid)

    def __ciphers_combo_handler(self, text: str):
        if(text == self.__ciphers_list[1] or text == self.__ciphers_list[2]):
            gpg_cipher_test = gpg_cipher("123", "AES256")
            if(gpg_cipher_test.check_gpg_insystem_exists() == False):
                ifMsg(self, "gpg is not installed! ", 4)
                self.__ciphers_combo.setCurrentIndex(self.__ciphers_combo_prev_index)
                return

        self.__ciphers_combo_prev_index = self.__ciphers_combo.currentIndex()

    def __file_src_pick_handler(self):
        curdir = str(os.path.abspath(os.getcwd()))
        file_prob_text = self.__file_src_text.text()
        if(file_prob_text != "" and (os.path.isfile(file_prob_text) == True or os.path.isdir(file_prob_text) == True)):
            file_prob_text = os.path.abspath(file_prob_text)
            curdir = os.path.dirname(file_prob_text)
        filepath = QFileDialog.getOpenFileName(self, "Select file", curdir)[0]
        filepath = os.path.abspath(filepath)
        self.__file_src_text.setText(filepath)

        if(self.__file_dest_text.text() == ""):
            self.__file_dest_text.setText(filepath + f".encrypted")

    def __file_dest_pick_handler(self):
        curdir = str(os.path.abspath(os.getcwd()))
        file_prob_text = self.__file_dest_text.text()
        if(file_prob_text != "" and (os.path.isfile(file_prob_text) == True or os.path.isdir(file_prob_text) == True)):
            file_prob_text = os.path.abspath(file_prob_text)
            curdir = os.path.dirname(file_prob_text)
        filepath = QFileDialog.getSaveFileName(self, "Select file", curdir)[0]
        filepath = os.path.abspath(filepath)
        self.__file_dest_text.setText(filepath)

    def set_en_de_Mutex(self, state: bool):
        self.__xcrypt_button_mutex = state


#https://stackoverflow.com/questions/26958644/qt-loading-indicator-widget
#          https://tenor.com/view/loading-buffering-spinning-waiting-gif-17313179
#          https://tenor.com/view/fox-reverse-minecraft-spinning-fox-spin-gif-21576621
    def show_msg(self, msg: str, type: int = 2):
        #ifMsg(self, msg, type)
        self.__info_msg_label.setText(msg)

    def __encrypt_button_handler(self):
        if(self.__xcrypt_button_mutex == True):
            ifMsg(self, f"File \"{self.__last_filename_src}\" is still being {self.cipher_mode} \nto \"{self.__last_filename_dest}\"... \nWait please", 2)
            return
        else:
            self.show_msg("")
            self.set_en_de_Mutex(True)
            try:
                path_in = self.__file_src_text.text()
                path_out = self.__file_dest_text.text()
                if(os.path.isfile(path_in) != True):
                    ifMsg(self, f"\"{path_in}\" is not file. ", 4)
                    self.set_en_de_Mutex(False)
                    return
                if(os.path.isdir(path_out) == True):
                    ifMsg(self, f"\"{path_out}\" is dirrectory", 4)
                    self.set_en_de_Mutex(False)
                    return
                path_in = os.path.abspath(path_in)
                path_out = os.path.abspath(path_out)
                if(path_in == path_out):
                    ifMsg(self, f"The same name \"{path_in}\" and \"{path_out}\"", 4)
                    self.set_en_de_Mutex(False)
                    return
                self.__last_filename_src, self.__last_filename_dest, self.cipher_mode = path_in, path_out, "encrypted"

                cipher_key = self.__pswd.get_password()
                if(cipher_key == ""):
                    ifMsg(self, "Fill passphrase", 4)
                    self.set_en_de_Mutex(False)
                    return
                if(check_passphrase_is_strong(cipher_key) == False):
                    out_text_warn_msg = "Your passphrase is not strong. \n"
                    out_text_warn_msg += "Passphrase must be long and \n"
                    out_text_warn_msg += "use in passphrase upper letters (\"ABC\"...) and lower letters (\"abc\"...) "
                    out_text_warn_msg += "and digits (\"123\"...) and symbols (\"?!%\"...)"
                    ifMsg(self, out_text_warn_msg, 3)
                
                cipher_combo_text = self.__ciphers_combo.currentText()
                if(cipher_combo_text == self.__ciphers_list[0]):
                    cipher = Pyca_Fernet(cipher_key)
                elif(cipher_combo_text == self.__ciphers_list[1]):
                    cipher = gpg_cipher(cipher_key, "AES256")
                elif(cipher_combo_text == self.__ciphers_list[2]):
                    cipher = gpg_cipher(cipher_key)
                elif(cipher_combo_text == self.__ciphers_list[3]):
                    cipher = kaes256CBC(cipher_key)
                else:
                    ifMsg(self, "Failed successfully. ", 4)
                    self.set_en_de_Mutex(False)
                    return
                
                self.show_msg(f"Encrypting {path_in} to {path_out}")
                x = threading.Thread(target=thread_func, args=(self, cipher, False, path_in, path_out,))
                x.start()
                ifMsg(self, f"File {path_in} started ecrypted to {path_out}. It may take some time...", 2)

            except:
                import traceback
                print(traceback.format_exc())
                ifMsg(self, "Cannot encrypt! ", 4)
                self.set_en_de_Mutex(False)

    def __decrypt_button_handler(self):
        if(self.__xcrypt_button_mutex == True):
            ifMsg(self, f"File \"{self.__last_filename_src}\" is still being {self.cipher_mode} \nto \"{self.__last_filename_dest}\"... \nWait please", 2)
            return
        else:
            self.__info_msg_label.setText("")
            self.set_en_de_Mutex(True)
            try:
                path_in = self.__file_src_text.text()
                path_out = self.__file_dest_text.text()
                if(os.path.isfile(path_in) != True):
                    ifMsg(self, f"\"{path_in}\" is not file. ", 4)
                    self.set_en_de_Mutex(False)
                    return
                if(os.path.isdir(path_out) == True):
                    ifMsg(self, f"\"{path_out}\" is dirrectory", 4)
                    self.set_en_de_Mutex(False)
                    return
                path_in = os.path.abspath(path_in)
                path_out = os.path.abspath(path_out)
                if(path_in == path_out):
                    ifMsg(self, f"The same name \"{path_in}\" and \"{path_out}\"", 4)
                    self.set_en_de_Mutex(False)
                    return
                self.__last_filename_src, self.__last_filename_dest, self.cipher_mode = path_in, path_out, "encrypted"

                cipher_key = self.__pswd.get_password()
                if(cipher_key == ""):
                    ifMsg(self, "Fill passphrase", 4)
                    self.set_en_de_Mutex(False)
                    return
                if(check_passphrase_is_strong(cipher_key) == False):
                    out_text_warn_msg = "Your passphrase is not strong. \n"
                    out_text_warn_msg += "Passphrase must be long and \n"
                    out_text_warn_msg += "use in passphrase upper letters (\"ABC\"...) and lower letters (\"abc\"...) "
                    out_text_warn_msg += "and digits (\"123\"...) and symbols (\"?!%\"...)"
                    ifMsg(self, out_text_warn_msg, 3)
                
                cipher_combo_text = self.__ciphers_combo.currentText()
                if(cipher_combo_text == self.__ciphers_list[0]):
                    cipher = Pyca_Fernet(cipher_key)
                elif(cipher_combo_text == self.__ciphers_list[1]):
                    cipher = gpg_cipher(cipher_key, "AES256")
                elif(cipher_combo_text == self.__ciphers_list[2]):
                    cipher = gpg_cipher(cipher_key)
                elif(cipher_combo_text == self.__ciphers_list[3]):
                    cipher = kaes256CBC(cipher_key)
                else:
                    ifMsg(self, "Failed successfully. ", 4)
                    self.set_en_de_Mutex(False)
                    return
                
                self.show_msg(f"Decrypting {path_in} to {path_out}")
                x = threading.Thread(target=thread_func, args=(self, cipher, True, path_in, path_out,))
                x.start()
                ifMsg(self, f"File {path_in} started derypted to {path_out}. It may take some time...", 2)

            except:
                import traceback
                print(traceback.format_exc())
                ifMsg(self, "Cannot encrypt! ", 4)
                self.set_en_de_Mutex(False)
