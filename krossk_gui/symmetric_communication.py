# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import ifMsg, PasswordWidget, HiddenLineEditWidget

class SymmetricCommunicationWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        self.__grid.addWidget(QLabel("Test", self), 0, 0, 1, 1)

        self.setLayout(self.__grid)

    def setPassphrase_ifEmpty(self, new_password: str):
        pass