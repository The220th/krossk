# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import ifMsg, PasswordWidget

from krossk_crypto import RSA4096, RSA4096_encrypt, utf8_to_bytes, bytes_to_utf8, Base64
from krossk_crypto import bytes_to_int, int_to_bytes, calc_hash, check_passphrase_is_strong, gen_password

class KeyExchangeWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()
        self.__grid.setHorizontalSpacing(25)

        self.__label_test = QLabel("", self)

        self.__genKeys_button = QPushButton("Generate keys \n(long process)", self)
        self.__genKeys_button.clicked.connect(lambda:self.__genKeys_button_handler())
        self.__pubKey_text_out = QLineEdit(self)
        self.__pubKey_text_out.setReadOnly(True)

        self.__key_text_in = PasswordWidget(self)
        self.__pubKey_text_in = QLineEdit(self)
        self.__pubKey_text_in.setReadOnly(False)
        self.__encrypt_button = QPushButton("Encrypt", self)
        self.__encrypt_button.clicked.connect(lambda:self.__encrypt_button_handler())
        #self.__encrypted_shakey_text_out = QLineEdit(self)
        #self.__encrypted_shakey_text_out.setReadOnly(True)
        self.__encrypted_key_text_out = QLineEdit(self)
        self.__encrypted_key_text_out.setReadOnly(True)
        self.__key_text_out2 = QLineEdit(self)
        self.__key_text_out2.setReadOnly(True)

        self.__encrypted_key_text_in = QLineEdit(self)
        self.__encrypted_key_text_in.setReadOnly(False)
        self.__deKeys_button = QPushButton("Form key", self)
        self.__deKeys_button.clicked.connect(lambda:self.__deKeys_button_handler())   
        self.__key_text_out1 = QLineEdit(self)
        self.__key_text_out1.setReadOnly(True)



        self.__grid.addWidget(QLabel("1. The first party:", self), 0, 0, 1, 1)
        self.__grid.addWidget(QLabel("2. The second party:", self), 0, 1, 1, 1)

        self.__grid.addWidget(QLabel("1.1. Generate keys:", self), 1, 0, 1, 1)
        self.__grid.addWidget(self.__genKeys_button, 2, 0, 1, 1)
        self.__grid.addWidget(QLabel("1.2. Send this public key to the second party:", self), 3, 0, 1, 1)
        self.__grid.addWidget(self.__pubKey_text_out, 4, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 5, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 6, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 7, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 8, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 9, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 10, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 11, 0, 1, 1)
        self.__grid.addWidget(QLabel("", self), 12, 0, 1, 1)
        self.__grid.addWidget(QLabel("1.3. Get encrypted passphrase from the second party:", self), 13, 0, 1, 1)
        self.__grid.addWidget(self.__encrypted_key_text_in, 14, 0, 1, 1)
        self.__grid.addWidget(QLabel("1.4. Decrypt:", self), 15, 0, 1, 1)
        self.__grid.addWidget(self.__deKeys_button, 16, 0, 1, 1)
        self.__grid.addWidget(QLabel("Use this shared passphrase:", self), 17, 0, 1, 1)
        self.__grid.addWidget(self.__key_text_out1, 18, 0, 1, 1)

        self.__grid.addWidget(QLabel("", self), 1, 1, 1, 1)
        self.__grid.addWidget(QLabel("", self), 2, 1, 1, 1)
        self.__grid.addWidget(QLabel("", self), 3, 1, 1, 1)
        self.__grid.addWidget(QLabel("", self), 4, 1, 1, 1)
        self.__grid.addWidget(QLabel("2.1 Input generator of shared passphrase: ", self), 5, 1, 1, 1)
        self.__grid.addWidget(self.__key_text_in, 6, 1, 1, 1)
        self.__grid.addWidget(QLabel("2.2. Get the public key from the first party and paste:", self), 7, 1, 1, 1)
        self.__grid.addWidget(self.__pubKey_text_in, 8, 1, 1, 1)
        self.__grid.addWidget(QLabel("2.3. Encrypt:", self), 9, 1, 1, 1)
        self.__grid.addWidget(self.__encrypt_button, 10, 1, 1, 1)
        self.__grid.addWidget(QLabel("2.4. Send this encrypted passphrase to the first party:", self), 11, 1, 1, 1)
        self.__grid.addWidget(self.__encrypted_key_text_out, 12, 1, 1, 1)
        self.__grid.addWidget(QLabel("", self), 13, 1, 1, 1)
        self.__grid.addWidget(QLabel("", self), 14, 1, 1, 1)
        self.__grid.addWidget(QLabel("", self), 15, 1, 1, 1)
        self.__grid.addWidget(QLabel("This shared passphrase below must be got by the first party.", self), 16, 1, 1, 1)
        self.__grid.addWidget(QLabel("Use this shared passphrase:", self), 17, 1, 1, 1)
        self.__grid.addWidget(self.__key_text_out2, 18, 1, 1, 1)


        self.setLayout(self.__grid)

    def __genKeys_button_handler(self):
        ifMsg(self, "It may take some time (a few minuts?)", 2)
        self.__rsa4096cipher = RSA4096()
        self.__pub_key = self.__rsa4096cipher.get_pub_key()
        self.__pubKey_text_out.setText(self.__pub_key)
    
    def __encrypt_button_handler(self):
        pubKey_text = self.__pubKey_text_in.text()
        key_text = self.__key_text_in.get_password()
        if(pubKey_text == ""):
            ifMsg(self, "Public key field is empty. Please fill it. ", 4)
            return
        if(key_text == ""):
            ifMsg(self, "Passphrase field is empty. Please fill it. ", 4)
            return
        if(check_passphrase_is_strong(key_text) == False):
            out_text_warn_msg = "Your passphrase is not strong. \n"
            out_text_warn_msg += "Passphrase must be long and \n"
            out_text_warn_msg += "use in passphrase upper letters (\"ABC\"...) and lower letters (\"abc\"...) "
            out_text_warn_msg += "and digits (\"123\"...) and symbols (\"?!%\"...)"
            ifMsg(self, out_text_warn_msg, 3)
        
        try:
            key_hash = calc_hash(key_text)
            #self.__encrypted_shakey_text_out.setText(key_hash)
            self.__key_text_out2.setText(key_hash)
            key_text_m = bytes_to_int(   utf8_to_bytes(key_hash)   )
            key_int_en = RSA4096_encrypt(pubKey_text, key_text_m)
            if(key_int_en == None):
                ifMsg(self, "Cannot encrypt! Invalid key?", 4)
                return
            bs64 = Base64()
            key_text_en = bs64.encode( int_to_bytes(key_int_en) )
            #key_text_en = str(key_int_en)

            self.__encrypted_key_text_out.setText(key_text_en)
        except:
            ifMsg(self, "Error! ", 4)
            return

    def __deKeys_button_handler(self):
        en_key_text = self.__encrypted_key_text_in.text()
        if(en_key_text == ""):
            ifMsg(self, "Encrypted passphrase is empty. Please fill it", 4)
            return
        try:
            bs64 = Base64()
            m = bytes_to_int(  bs64.decode(en_key_text)  )
            #m = int(en_key_text)
            
            key_m = self.__rsa4096cipher.decrypt(m)
            if(key_m == None):
                ifMsg(self, "Cannot encrypt! Invalid key?", 4)
                return
            res = bytes_to_utf8(   int_to_bytes(key_m)   )
            self.__key_text_out1.setText(res)
        except:
            ifMsg(self, "Error! ", 4)
            return