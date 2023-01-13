# -*- coding: utf-8 -*-

import PIL
from PIL import Image as PIL_Image
from PIL import ImageQt as PIL_ImageQt
from io import BytesIO

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QDialog, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from krossk_crypto import gen_password

def ifMsg(parent, text: str, type: int, MODAL: bool = True):
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

def exe_widget_in_QDialog(parent, widget: "QWidget", MODAL: bool = True):
    msg = QDialog(parent)
    msg.setModal(MODAL)

    grid = QGridLayout()

    exitButton = QPushButton(ico_get_exit(), "Done", msg)
    exitButton.clicked.connect(lambda:msg.close())

    grid.addWidget(widget, 0, 0, 1, 1)
    grid.addWidget(exitButton, 1, 0, 1, 1)

    msg.setLayout(grid)
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
    
    def get_password(self) -> str:
        return self.__password_text.text()

    def set_password(self, pswd: str):
        self.__password_text.setText(pswd)

    def __passwd_echo_checkbox_handler(self):
        if(self.__passwd_echo_checkbox.isChecked() == False):
            self.__password_text.setEchoMode(QLineEdit.Password)
        else:
            self.__password_text.setEchoMode(QLineEdit.Normal)
    
    def __rnd_passwd_button_handler(self):
        self.__password_text.setText(gen_password())

class HiddenLineEditWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        self.__hidden_text = QLineEdit(self)
        self.__hidden_text.setReadOnly(False)
        self.__hidden_text.setEchoMode(QLineEdit.Password)

        self.__passwd_echo_checkbox = QCheckBox("Show", self)
        self.__passwd_echo_checkbox.setChecked(False)
        self.__passwd_echo_checkbox.toggled.connect(lambda:self.__passwd_echo_checkbox_handler())

        self.__grid.addWidget(self.__hidden_text, 0, 0, 1, 1)
        self.__grid.addWidget(self.__passwd_echo_checkbox, 0, 1, 1, 1)

        self.setLayout(self.__grid)
    
    def get_text(self) -> str:
        return self.__hidden_text.text()
    
    def set_text(self, txt: str):
        self.__hidden_text.setText(txt)

    def __passwd_echo_checkbox_handler(self):
        if(self.__passwd_echo_checkbox.isChecked() == False):
            self.__hidden_text.setEchoMode(QLineEdit.Password)
        else:
            self.__hidden_text.setEchoMode(QLineEdit.Normal)













def ico_get_rnd() -> "QIcon":
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x58\x49\x44\x41\x54\x38\x8d\x63\x60\xa0\x01\x60\x84\xd2\xff\x69\x60\x26\xd5\x0c\xfd\xcf\xc0\xc0\xc0\xc0\x44\x25\xc3\x50\x00\x0b\x2e\xdb\xa0\x80\x11\x8b\x3c\x41\x40\x13\x97\xd2\xcd\xfb\x64\x79\x19\x19\xd0\xcd\xa5\xd8\x00\x49\x91\x37\xb4\x23\x0a\x1b\x20\x29\xf2\x06\xd4\xa5\xd8\x00\xce\xc8\x1b\x7e\x11\x85\x0d\xe0\x8c\x3c\x9a\xbb\x94\x9a\xa5\x3f\xf5\x01\x00\xa2\xa7\x07\x32\xd7\xbd\xca\x1f\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon

def ico_get_exit() -> "QIcon":
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x93\x49\x44\x41\x54\x38\x8d\xbd\x94\x51\x0e\x80\x20\x0c\x43\x8b\xf1\xe0\xdc\x1c\x7f\xd4\xcc\xb9\xba\x02\x6a\x13\x12\xd8\xdc\xcb\x60\x8d\xc0\x07\x2a\x66\xdf\x5e\xe2\x5c\x34\x02\x6d\x66\x9d\x5a\x66\x8a\x77\x15\xf3\x4d\x17\x14\x00\x50\x6b\x65\xa9\x1b\x18\x2c\xe0\x72\x51\xa7\xe1\x79\x4d\x9a\xf3\x45\x74\x20\x56\x4f\xd7\x8f\x3a\x97\x86\x99\xbd\x69\xd4\x59\x0a\x66\x50\x56\x48\x07\xa2\x40\x2d\x40\x8d\x4b\xd0\x4c\xb4\x5b\x06\xcd\xae\x29\xb9\x80\x01\x24\x5f\x9a\x7d\x03\xfa\x2d\x55\x48\xfc\xc8\x01\xb8\x9b\x7f\xc8\xec\x5e\x1e\x3a\x04\xf1\x9a\x99\xfe\xbf\xd0\x59\xf9\x3f\x57\x3a\x7d\x45\xa1\x9f\x37\x4c\x39\x26\x90\x04\x60\x34\x39\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon

def ico_get_chat() -> "QIcon":
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x6e\x49\x44\x41\x54\x38\x8d\xcd\x93\x4b\x0e\xc0\x20\x08\x05\x9f\x8d\xf7\xbf\x32\xdd\x35\x82\xa8\x84\x8f\xe9\xac\x94\x84\x11\x08\x02\x05\xb4\xe1\x4c\x49\x1e\x26\xf4\x4a\x97\xb9\x91\x2a\xa7\xfc\x27\x28\x53\x59\x49\x65\x4b\xa7\xbb\x49\x9a\xc2\x6f\x67\xfa\x8d\xa4\x89\x57\xd4\x7d\x33\xc8\x98\xab\x62\xf9\x99\x87\xb4\xa0\x03\xea\x07\xc9\xd8\x9a\xe5\x0e\x00\xe8\x32\x50\x45\xb8\xfd\xeb\xdf\xd4\xc3\xb4\x52\x19\xd2\x9d\xd3\xcd\xb6\xd2\x90\xb4\x84\x17\x4e\xba\x23\xff\x95\xbc\x5f\xcd\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon

def ico_get_chat_in() -> "QIcon":
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x6e\x49\x44\x41\x54\x38\x8d\xd5\x94\x41\x0a\xc0\x20\x0c\x04\xb7\xa5\xff\xff\x72\x7b\x51\x90\x82\x71\x36\x5a\xb0\x7b\xf1\x60\x1c\x93\x8d\x46\xfa\x8b\x8e\xb2\xde\x20\xc6\x56\x04\xb5\x75\x26\x2e\x1f\x26\xe0\x40\x2b\x6c\x68\x07\x85\x62\xa0\x24\x5d\x09\x20\x6e\x6a\x2f\x10\x79\xf8\x56\x54\xbe\x55\x32\x81\xa6\x81\x11\x94\xf8\x67\x43\xa7\xc0\xed\xc1\x5e\xa9\xcb\xbb\xdf\xee\xe3\x8c\xe9\xe3\xb7\xac\x70\xbe\xa9\xed\xf1\xd2\x29\xf5\xe9\x3c\xdd\x5f\x0f\x2b\xd5\x19\x10\x07\x14\xaf\xd3\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon

def ico_get_chat_out() -> "QIcon":
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x6d\x49\x44\x41\x54\x38\x8d\xd5\x94\xcd\x0e\x00\x10\x0c\x83\x11\xef\xff\xca\x5c\x1c\x16\x9a\xfd\x14\x09\xbd\x88\xa4\xf9\x6c\x6b\x26\xa5\x5f\x94\xc7\xd9\x1c\x9e\xb0\x34\x68\x58\x85\x78\xdc\x2c\x20\x0a\xf5\x8c\x2b\x0c\x75\x81\xa5\x41\x06\xe2\x09\xae\x4d\xf7\x45\x6c\x50\x70\xc6\x4c\xfb\x52\x70\x14\xbb\x50\x08\x3e\x01\x5d\x66\xbb\x0b\x85\x61\x55\xc3\x8c\x74\x2d\x7d\x75\xb3\x98\xf6\xcd\x0a\x99\xdd\x57\x81\xc8\x7c\x44\x57\xff\xd3\xf7\xd5\x01\x0c\x4a\x19\x10\x3e\xf0\xcc\xa5\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon

def ico_get_file() -> "QIcon":
    imageBytes = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x15\x00\x00\x00\x15\x08\x06\x00\x00\x00\xa9\x17\xa5\x96\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95\x2b\x0e\x1b\x00\x00\x00\x6b\x49\x44\x41\x54\x38\x8d\xed\x94\xc1\x0e\xc0\x20\x08\x43\x75\xd9\xff\xff\x32\x5e\x16\x13\x18\x16\x0a\x57\xdf\xc5\x44\xa0\x29\x41\x9c\x43\x23\x83\x67\xa2\xa0\x90\xa2\x62\x4e\x98\xc4\x8a\xfe\x6a\xdf\xa4\x38\x6c\xf1\x8b\x8b\x97\xd7\x71\xaa\xee\x1e\x52\x28\x85\xd7\x3e\x43\xd8\x5d\xe5\x39\xb9\x1a\xd9\x41\x45\xa8\x01\x79\xa2\xd1\xa4\x43\xae\x53\x9c\x50\xe1\x3a\xc5\x09\x15\xec\x87\xd2\x59\xd5\x5d\x6b\x5d\x75\xf7\xbf\xdd\xe5\x91\x05\x1c\x75\x18\x2e\x63\x5e\xd1\x08\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    stream = BytesIO(imageBytes)
    image = PIL_Image.open(stream).convert("RGBA")
    stream.close()
    image_image_qt = PIL_ImageQt.ImageQt(image)
    pixmap = QPixmap.fromImage(image_image_qt)
    icon = QIcon(pixmap)
    return icon

def ico_get_main() -> "QIcon":
    svg_str="""<?xml version="1.0"?>
<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" version="1.0">
 <g class="layer">
  <title>Layer 1</title>
  <g id="svg_27">
   <g fill="#E65A5AFF" id="svg_1" stroke="#E65A5AFF" stroke-opacity="0">
    <path d="m216.97,264.08c8.3,9.98 8.12,19.91 -0.53,29.78c-8.59,9.76 -23.19,15.89 -45.83,19.19l-18.21,2.65l0,87.92c0,55.77 0.8,88.41 2.19,89.27c3.4,2.1 34.92,-2.87 50.09,-7.88c7.5,-2.5 17.77,-7.5 22.81,-11.15c16.27,-11.79 16.11,-9.94 8.67,-108.16c-3.59,-47.81 -7.66,-89.68 -9.02,-93.06c-1.35,-3.36 -5.56,-8.3 -9.33,-10.98l-6.89,-4.85l6.06,7.28" fill="#ff7f00" id="svg_2" stroke="#000000"/>
   </g>
   <g fill="#EB7373FF" id="svg_3" stroke="#EB7373FF" stroke-opacity="0">
    <path d="m87.3,266.81c-3.33,3.71 -6.51,8.92 -7.07,11.57c-1.3,6.36 -12.37,159.1 -12.29,170.08c0.06,12.43 6.89,21.76 21.54,29.54c15.72,8.34 27.88,11.7 48.7,13.49l16.09,1.39l-0.13,-88.61l-0.15,-88.61l-4.93,-1.3c-2.72,-0.72 -7.54,-1.35 -10.77,-1.38c-3.2,0 -12.38,-2.06 -20.41,-4.53c-27,-8.34 -38.92,-26.2 -28.37,-42.47c3.45,-5.3 3.2,-5.21 -2.2,0.81" fill="#f29137" id="svg_4" stroke="#000000"/>
   </g>
   <g fill="#E65A5AFF" id="svg_5" stroke="#E65A5AFF" stroke-opacity="0">
    <path d="m371.59,107.4l-55.59,55.74l7.5,8.83c11.06,13 18.71,30.04 18.71,41.61c0,13.36 -1.66,16.86 -9.72,20.35l-6.85,2.97l5.89,0.09c6.76,0.1 3.4,2.72 74.06,-57.84c29.38,-25.21 54.58,-47.99 56,-50.62c3.71,-6.95 1.11,-25.84 -5.47,-39.64c-5.68,-11.92 -24.26,-37.23 -27.32,-37.23c-0.9,0 -26.67,25.07 -57.25,55.74" fill="#8f4dd1" id="svg_6" stroke="#000000"/>
   </g>
   <g fill="#EB7373FF" id="svg_7" stroke="#EB7373FF" stroke-opacity="0">
    <path d="m353.68,19.41c-2.06,0.59 -27.63,28.92 -56.85,62.91c-41.34,48.12 -53.06,63.1 -53,67.72l0.09,5.93l2.97,-6.85c3.46,-7.97 7.04,-9.73 19.64,-9.67c10.95,0.06 24.45,5.83 39.5,16.86l10.95,8.03l56.2,-56.06l56.2,-56.06l-9.5,-8.37c-18.85,-16.6 -51.74,-28.74 -66.22,-24.45" fill="#9d66dd" id="svg_8" stroke="#000000"/>
   </g>
   <g fill="#A0C8AAFF" id="svg_11" stroke="#A0C8AAFF">
    <path d="m159.5,244.76c-2.72,1.67 -3.31,9.33 -2.28,29.58c0.18,3.64 -0.24,13.98 -0.93,22.96l-1.26,16.36l14.16,-1.33c27.16,-2.54 50.23,-15.1 53.8,-29.24c2.54,-10.13 -4.67,-20.8 -18.98,-27.99c-13.77,-6.94 -40.1,-13.05 -44.49,-10.32" id="svg_12"/>
   </g>
   <g fill="#C8DCC8FF" id="svg_13" stroke="#C8DCC8FF">
    <path d="m127.85,247.04c-12.56,2.28 -25.89,8.79 -34.76,17c-4.72,4.36 -6.06,7.62 -6.06,14.72c0,10.99 6.55,18.28 23.05,25.56c10.4,4.59 49.47,11.92 51.7,9.72c0.58,-0.58 -0.68,-1.07 -2.78,-1.07c-3.33,0 -3.76,-2.1 -3.31,-16.01c0.28,-8.8 -0.15,-15.75 -0.95,-15.46c-0.81,0.31 -2.38,0.55 -3.51,0.55c-3.09,0 -7.07,-21.74 -5.5,-30.1c1.57,-8.39 1.43,-8.42 -17.85,-4.93" fill="null" fill-opacity="null" id="svg_14" stroke="null" stroke-dasharray="null" stroke-linecap="null" stroke-linejoin="null" stroke-opacity="null" stroke-width="null"/>
   </g>
   <g fill="#C8DCC8FF" id="svg_15" stroke="#C8DCC8FF">
    <path d="m255.46,140.68c-15.16,6.49 -11.17,34.94 8.17,57.81l6.27,7.41l11.83,-11.58c6.49,-6.38 12.82,-11.58 14.07,-11.58c1.24,0 6.15,-4.07 10.98,-9.01l8.71,-9.01l-7.31,-6.18c-17.53,-14.76 -41.17,-22.78 -52.72,-17.85" id="svg_16"/>
   </g>
   <g fill="#A0C8AAFF" id="svg_17" stroke="#A0C8AAFF">
    <path d="m307.2,173.28c-4.79,4.94 -8.28,10.71 -8.28,13.73c0,3.24 -3.99,9.16 -10.75,15.93l-10.77,10.75l6.91,5.83c10.44,8.83 27.81,16.14 38.43,16.15c7.26,0.01 10.81,-1.3 15.19,-5.65c4.9,-4.93 5.55,-7.13 4.67,-16.14c-1.21,-12.65 -8.96,-28.79 -19.41,-40.49l-7.72,-8.65l-8.28,8.52" id="svg_18"/>
   </g>
   <g fill="#A0C8AAFF" id="svg_19" stroke="#A0C8AAFF">
    <path d="m243.75,448.82c0,18.79 -20.9,34.79 -54.88,41.98c-8.06,1.7 -18.87,3.11 -24.04,3.14c-9.23,0.04 -9.38,0.18 -9.38,7.66c0,7.46 -0.18,7.62 -10.49,8.55c-5.75,0.53 1.43,0.67 16.01,0.31c31.03,-0.72 54.52,-7.03 73.15,-19.63c22.16,-14.98 30.59,-42.38 15.19,-49.41c-5.5,-2.5 -5.56,-2.43 -5.56,7.4" id="svg_20"/>
   </g>
   <g fill="#C8DCC8FF" id="svg_21" stroke="#C8DCC8FF">
    <path d="m57.57,445.04c-8.61,9.5 -0.5,31.85 15.52,42.91c18.25,12.63 47.13,21.37 70.77,21.43l11.58,0.04l0,-7.72l0,-7.72l-10.49,-0.04c-14.9,-0.04 -37.93,-5.33 -51.71,-11.85c-17.04,-8.08 -26.32,-18.42 -27.72,-30.95c-1.26,-11.15 -2.51,-12.11 -7.94,-6.09" id="svg_22"/>
   </g>
   <g fill="#A0C8AAFF" id="svg_23" stroke="#A0C8AAFF" transform="matrix(2.20739, -0.0114509, 0.0114509, 2.20739, -98.6663, -205.232)">
    <path d="m241.54,114.42l-2.32,2.46l5.11,6.67c6.27,8.18 7.67,10.82 9.57,18.13c1.71,6.55 0.82,11.87 -2.46,14.84c-2.34,2.12 -1.8,3.53 1.35,3.53c4.41,0 8.62,-6.79 8.62,-13.88c0,-8.18 -5.53,-20.04 -14.03,-30.06l-3.53,-4.16l-2.31,2.47" id="svg_24"/>
   </g>
   <g fill="#C8DCC8FF" id="svg_25" stroke="#C8DCC8FF">
    <path d="m347.5,8.76c-5.92,4.02 -7.9,7.04 -8.46,12.88l-0.72,7.66l5.34,-5.01c11.54,-10.84 28.39,-10.55 51.2,0.89c13.71,6.86 23.93,14.44 35.29,26.09c4.79,4.93 6.86,6.69 4.62,3.95c-4.02,-4.88 -3.99,-5.1 0.72,-10.13l4.81,-5.12l-13.4,-10.53c-20.84,-16.37 -37.62,-23.84 -56.05,-24.98c-13.73,-0.84 -16.55,-0.33 -23.36,4.3" id="svg_26"/>
   </g>
   <g fill="#FFD25AFF" id="svg_9" stroke="#FFD25AFF">
    <path d="m164.16,99.97c-4.59,3.15 -11.15,10.67 -14.61,16.6c-5.59,9.72 -6.24,13.02 -6.24,31.48c0,24.02 2.88,31.66 18.7,49.55l10.22,11.57l-7.19,5.72c-9.67,7.72 -15.87,20.75 -17.53,37.02c-1.52,14.94 2.12,30.15 7.19,30.15c2.59,0 2.93,-3.22 1.79,-17c-1.3,-15.68 -0.95,-17.84 4.57,-27.41c3.31,-5.72 9.32,-12.97 13.37,-16.14l7.37,-5.72l14.53,6.09c11.39,4.76 18.16,6.06 31.39,6.02c24.48,-0.1 39.86,-6.76 59.07,-25.61c15.83,-15.55 17.32,-18.06 11.97,-20.13c-1.94,-0.75 -6.54,2.47 -11.48,8.03c-10,11.26 -34.84,24.36 -50.26,26.54c-11.08,1.57 -32.03,-1.48 -38.46,-5.59c-2.6,-1.66 -1.38,-4.16 6.41,-12.69c5.3,-5.87 12.19,-16.32 15.28,-23.24c11.21,-24.9 3.8,-59.94 -15.69,-74.33c-12.16,-8.96 -28.25,-9.32 -40.4,-0.93m34.2,9.98c9.64,7.16 15.84,22.19 15.84,38.55c0,17.17 -3.22,25.83 -14.57,39.1c-14.16,16.58 -15.69,16.69 -29.45,1.89c-14.3,-15.41 -17.53,-24.21 -16.37,-44.76c1.79,-32.03 24.35,-49.64 44.54,-34.76" id="svg_10"/>
   </g>
  </g>
 </g>

</svg>
"""
    svg_bytes = bytearray(svg_str, encoding='utf-8')
    qimage = QImage.fromData(svg_bytes)
    #icon = QIcon(QPixmap.fromImage(qimage).scaled(QtCore.QSize(500, 500)))
    icon = QIcon(QPixmap.fromImage(qimage))
    return icon