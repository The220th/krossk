# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import PasswordWidget, ifMsg
from . import ico_get_file

from krossk_crypto import pycrypto_cipher, gpg_cipher, check_passphrase_is_strong

import os
import threading

def thread_func(parent: "QWidget"):
    pass

class FileTransferWidget(QWidget):

    __xcrypt_button_mutex = False
    __ciphers_list = ["pycrypto AES256-cbc", "gpg AES256"] # порядок не менять! 

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        self.__pswd = PasswordWidget(self)

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
        self.__grid.addWidget(buffWidget, 3, 0, 1, 2)

        self.setLayout(self.__grid)

    def __ciphers_combo_handler(self, text: str):
        if(text == self.__ciphers_list[1]):
            gpg_cipher_test = gpg_cipher("123")
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

    def __file_dest_pick_handler(self):
        curdir = str(os.path.abspath(os.getcwd()))
        file_prob_text = self.__file_dest_text.text()
        if(file_prob_text != "" and (os.path.isfile(file_prob_text) == True or os.path.isdir(file_prob_text) == True)):
            file_prob_text = os.path.abspath(file_prob_text)
            curdir = os.path.dirname(file_prob_text)
        filepath = QFileDialog.getSaveFileName(self, "Select file", curdir)[0]
        filepath = os.path.abspath(filepath)
        self.__file_dest_text.setText(filepath)

    def __encrypt_button_handler(self):
        pass

    def __decrypt_button_handler(self):
        pass