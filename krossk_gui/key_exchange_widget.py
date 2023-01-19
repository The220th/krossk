# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import ifMsg, PasswordWidget, HiddenLineEditWidget

from krossk_crypto import kRSA4096, RSA4096_encrypt, utf8_to_bytes, bytes_to_utf8, Base64
from krossk_crypto import bytes_to_int, int_to_bytes, calc_hash_512, check_passphrase_is_strong

from cryptography.hazmat.primitives.asymmetric.x448 import X448PublicKey
from cryptography.hazmat.primitives.asymmetric.x448 import X448PrivateKey
from cryptography.hazmat.primitives import serialization

import base64

class KeyExchangeWidget(QWidget):

    __variantsToChoose = ["pyca X448", "kRSA4096"] # порядок не менять!

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        self.__pyca_x448 = one_KeyExchangeWidget(1, self)
        self.__krsa = one_KeyExchangeWidget(2, self)

        self.__stackedWidget = QStackedWidget(self)
        self.__stackedWidget.addWidget(self.__pyca_x448)
        self.__stackedWidget.addWidget(self.__krsa)

        self.__widgetsSelectCombo = QComboBox(self)
        self.__widgetsSelectCombo.addItems(self.__variantsToChoose)
        self.__widgetsSelectCombo.activated[str].connect(self.__widgetsSelectComboActivated)

        self.__grid.addWidget(self.__widgetsSelectCombo, 0, 0, 1, 1)
        self.__grid.addWidget(self.__stackedWidget, 1, 0, 1, 1)

        self.setLayout(self.__grid)

    def __widgetsSelectComboActivated(self, text: str):
        i = 0
        for var_i in self.__variantsToChoose:
            if(text == var_i):
                break
            i-=-1
        self.__stackedWidget.setCurrentIndex(i)

class one_KeyExchangeWidget(QWidget):

    def __init__(self, algo_num, parent):
        if(not (algo_num == 1 or algo_num == 2)):
            raise AttributeError(f"No such algorithm: {algo_num}")
        self.__algo_num = algo_num
        super().__init__(parent)

        self.__grid = QGridLayout()
        self.__grid.setHorizontalSpacing(25)

        if(self.__algo_num == 2):
            self.__genKeys_button = QPushButton("Generate keys \n(long process)", self)
        else:
            self.__genKeys_button = QPushButton("Generate keys", self)
        self.__genKeys_button.clicked.connect(lambda:self.__genKeys_button_handler())
        self.__pubKey_text_out = QLineEdit(self)
        self.__pubKey_text_out.setReadOnly(True)

        if(self.__algo_num == 2):
            self.__key_text_in = PasswordWidget(self)
        self.__pubKey_text_in = QLineEdit(self)
        self.__pubKey_text_in.setReadOnly(False)
        if(self.__algo_num == 1):
            self.__encrypt_button = QPushButton("Generate keys", self)
        elif(self.__algo_num == 2):
            self.__encrypt_button = QPushButton("Encrypt", self)
        else:
            ifMsg(self, "Failed successfully", 4)
        self.__encrypt_button.clicked.connect(lambda:self.__encrypt_button_handler())
        #self.__encrypted_shakey_text_out = QLineEdit(self)
        #self.__encrypted_shakey_text_out.setReadOnly(True)
        self.__encrypted_key_text_out = QLineEdit(self)
        self.__encrypted_key_text_out.setReadOnly(True)
        self.__key_text_out2 = HiddenLineEditWidget(self)

        self.__encrypted_key_text_in = QLineEdit(self)
        self.__encrypted_key_text_in.setReadOnly(False)
        self.__deKeys_button = QPushButton("Form key", self)
        self.__deKeys_button.clicked.connect(lambda:self.__deKeys_button_handler())   
        self.__key_text_out1 = HiddenLineEditWidget(self)



        self.__grid.addWidget(QLabel("1. The first party:", self), 0, 0, 1, 1)
        self.__grid.addWidget(QLabel("2. The second party:", self), 0, 1, 1, 1)
        if(self.__algo_num == 1):
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
            self.__grid.addWidget(QLabel("1.3. Get public key from the second party and paste:", self), 11, 0, 1, 1)
            self.__grid.addWidget(self.__encrypted_key_text_in, 12, 0, 1, 1)
            self.__grid.addWidget(QLabel("1.4. Decrypt:", self), 13, 0, 1, 1)
            self.__grid.addWidget(self.__deKeys_button, 14, 0, 1, 1)
            self.__grid.addWidget(QLabel("Use this shared passphrase:", self), 15, 0, 1, 1)
            self.__grid.addWidget(self.__key_text_out1, 16, 0, 1, 1)

            self.__grid.addWidget(QLabel("", self), 1, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 2, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 3, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 4, 1, 1, 1)
            self.__grid.addWidget(QLabel("2.1. Get the public key from the first party and paste:", self), 5, 1, 1, 1)
            self.__grid.addWidget(self.__pubKey_text_in, 6, 1, 1, 1)
            self.__grid.addWidget(QLabel("2.2. Generate keys:", self), 7, 1, 1, 1)
            self.__grid.addWidget(self.__encrypt_button, 8, 1, 1, 1)
            self.__grid.addWidget(QLabel("2.3. Send this public key to the first party:", self), 9, 1, 1, 1)
            self.__grid.addWidget(self.__encrypted_key_text_out, 10, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 11, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 12, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 13, 1, 1, 1)
            self.__grid.addWidget(QLabel("", self), 14, 1, 1, 1)
            self.__grid.addWidget(QLabel("Use this shared passphrase:", self), 15, 1, 1, 1)
            self.__grid.addWidget(self.__key_text_out2, 16, 1, 1, 1)
        elif(self.__algo_num == 2):
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
            self.__grid.addWidget(QLabel("1.4. Calculate shared passphrase:", self), 15, 0, 1, 1)
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
        else:
            ifMsg(self, "Failed successfully", 4)

        self.setLayout(self.__grid)

    def __genKeys_button_handler(self):
        if(self.__algo_num == 1):
            self.__private_key1 = X448PrivateKey.generate()
            public_key1 = self.__private_key1.public_key()
            #self.__private_key1_text = self.__private_key1.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())
            public_key1_bytes = public_key1.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
            public_key1_text = base64.b64encode(public_key1_bytes).decode("ascii")
            self.__pubKey_text_out.setText(public_key1_text)
        elif(self.__algo_num == 2):
            ifMsg(self, "It may take some time (a few minuts?)", 2)
            self.__rsa4096cipher = kRSA4096()
            self.__pub_key = self.__rsa4096cipher.get_pub_key()
            self.__pubKey_text_out.setText(self.__pub_key)
        else:
            ifMsg(self, "Failed successfully", 4)

    
    def __encrypt_button_handler(self):
        pubKey_text = self.__pubKey_text_in.text()
        if(self.__algo_num == 2):
            key_text = self.__key_text_in.get_password()
        if(pubKey_text == ""):
            ifMsg(self, "Public key field is empty. Please fill it. ", 4)
            return
        if(self.__algo_num != 1 and key_text == ""):
            ifMsg(self, "Passphrase field is empty. Please fill it. ", 4)
            return
        if(self.__algo_num != 1 and check_passphrase_is_strong(key_text) == False):
            out_text_warn_msg = "Your passphrase is not strong. \n"
            out_text_warn_msg += "Passphrase must be long and \n"
            out_text_warn_msg += "use in passphrase upper letters (\"ABC\"...) and lower letters (\"abc\"...) "
            out_text_warn_msg += "and digits (\"123\"...) and symbols (\"?!%\"...)"
            ifMsg(self, out_text_warn_msg, 3)
        
        try:
            if(self.__algo_num == 1):
                privkey2 = X448PrivateKey.generate()
                pubkey2 = privkey2.public_key()
                pubkey2_bytes = pubkey2.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
                pubkey2_text = base64.b64encode(pubkey2_bytes).decode("ascii")
                self.__encrypted_key_text_out.setText(pubkey2_text)

                pubkey1_bytes = base64.b64decode(pubKey_text.encode("ascii"))
                pubkey1 = X448PublicKey.from_public_bytes(pubkey1_bytes)

                shared_key = privkey2.exchange(pubkey1)
                self.__key_text_out2.set_text(base64.b64encode(shared_key).decode("ascii"))
            elif(self.__algo_num == 2):
                key_hash = calc_hash_512(key_text)[1]
                #self.__key_text_out2.set_text(key_hash)
                self.__key_text_out2.set_text(base64.b64encode(key_hash).decode("ascii"))
                #key_text_m = bytes_to_int(   utf8_to_bytes(key_hash)   )
                key_text_m = bytes_to_int(   key_hash   )
                key_int_en = RSA4096_encrypt(pubKey_text, key_text_m)
                if(key_int_en == None):
                    ifMsg(self, "Cannot encrypt! Invalid key?", 4)
                    return
                bs64 = Base64()
                key_text_en = bs64.encode( int_to_bytes(key_int_en) )
                #key_text_en = str(key_int_en)

                self.__encrypted_key_text_out.setText(key_text_en)
            else:
                ifMsg(self, "Failed successfully", 4)
        except:
            import traceback
            print(traceback.format_exc())
            ifMsg(self, "Error! ", 4)
            return

    def __deKeys_button_handler(self):
        en_key_text = self.__encrypted_key_text_in.text()
        if(en_key_text == ""):
            ifMsg(self, "Encrypted passphrase is empty. Please fill it", 4)
            return
        try:
            if(self.__algo_num == 1):
                pubkey2_bytes = base64.b64decode(en_key_text.encode("ascii"))
                pubkey2 = X448PublicKey.from_public_bytes(pubkey2_bytes)

                shared_key = self.__private_key1.exchange(pubkey2)
                self.__key_text_out1.set_text(base64.b64encode(shared_key).decode("ascii"))
            elif(self.__algo_num == 2):
                bs64 = Base64()
                m = bytes_to_int(  bs64.decode(en_key_text)  )
                #m = int(en_key_text)
                
                key_m = self.__rsa4096cipher.decrypt(m)
                if(key_m == None):
                    ifMsg(self, "Cannot encrypt! Invalid key?", 4)
                    return
                #res = bytes_to_utf8(   int_to_bytes(key_m)   )
                res = base64.b64encode(  int_to_bytes(key_m)  ).decode("ascii")
                self.__key_text_out1.set_text(res)
            else:
                ifMsg(self, "Failed successfully", 4)
        except:
            import traceback
            print(traceback.format_exc())
            ifMsg(self, "Error! ", 4)
            return