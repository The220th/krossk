# -*- coding: utf-8 -*-

import PIL
from PIL import Image as PIL_Image
from PIL import ImageQt as PIL_ImageQt
from io import BytesIO

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from krossk_crypto import gen_password

def ifMsg(parent, text : str, type : int, MODAL:bool = True):
    '''
    0 - None
    1 - Question
    2 - Information
    3 - Warning
    4 - Critical
    '''
    msg = QMessageBox(parent)

    if(type == 0):
        msg.setWindowTitle("")
    elif(type == 1):
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Question")
    elif(type == 2):
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
    elif(type == 3):
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
    elif(type == 4):
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")

    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setModal(MODAL)
    msg.exec()

class PasswordWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        self.__password_text = QLineEdit(self)
        self.__password_text.setReadOnly(False)
        self.__password_text.setEchoMode(QLineEdit.Password)

        self.__passwd_echo_checkbox = QCheckBox("Show", self)
        self.__passwd_echo_checkbox.setChecked(False)
        self.__passwd_echo_checkbox.toggled.connect(lambda:self.__passwd_echo_checkbox_handler())

        self.__rnd_passwd_button = QPushButton(ico_get_rnd(), "Rnd", self)
        self.__rnd_passwd_button.clicked.connect(lambda:self.__rnd_passwd_button_handler())

        self.__grid.addWidget(self.__password_text, 0, 0, 1, 1)
        self.__grid.addWidget(self.__passwd_echo_checkbox, 0, 1, 1, 1)
        self.__grid.addWidget(self.__rnd_passwd_button, 0, 2, 1, 1)

        self.setLayout(self.__grid)
    
    def get_password(self):
        return self.__password_text.text()

    def __passwd_echo_checkbox_handler(self):
        if(self.__passwd_echo_checkbox.isChecked() == False):
            self.__password_text.setEchoMode(QLineEdit.Password)
        else:
            self.__password_text.setEchoMode(QLineEdit.Normal)
    
    def __rnd_passwd_button_handler(self):
        self.__password_text.setText(gen_password())















def ico_get_rnd():
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x50\x49\x44\x41\x54\x38\x8d\x63\x60\xa0\x01\x60\x84\xd2\xff\x69\x60\x26\xd5\x0c\xfd\xcf\xc0\xc0\xc0\xc0\x82\x4d\x10\xdd\x46\x52\x01\x13\xb9\x1a\xe9\x6e\x28\xba\xf7\xc9\xf6\x32\x32\x18\xba\xde\xc7\x05\x48\x4a\x15\xc3\xcf\xfb\x24\xa5\x8a\xe1\xe7\x7d\x5c\x00\x6b\xaa\x18\x39\xde\xc7\x9a\x2a\x90\x0d\xa5\x66\xe9\x4f\x7d\x00\x00\xa2\xa7\x07\x32\x65\xf2\x1f\xd6\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon