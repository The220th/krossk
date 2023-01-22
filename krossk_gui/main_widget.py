# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget, QTabWidget, QScrollArea)

from . import KeyExchangeWidget, SymmetricCommunicationWidget, FileTransferWidget, HelpWidget, ico_get_question

class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.__grid = QGridLayout()

        self.__key_exchange_widget = KeyExchangeWidget(self)
        self.__symmetric_communication_widget = SymmetricCommunicationWidget(self)
        self.__file_transfer_widget = FileTransferWidget(self)
        self.__help_widget = HelpWidget(self)

        self.__tabs = QTabWidget(self)
        self.__tabs.resize(300, 200)
        self.__tabs.addTab(self.__key_exchange_widget, "Key exchange")
        self.__tabs.addTab(self.__symmetric_communication_widget, "Symmetric communication")
        self.__tabs.addTab(self.__file_transfer_widget, "Encrypt/decrypt file")
        # SP_MessageBoxQuestion
        self.__tabs.addTab(self.__help_widget, ico_get_question(), "Help")

        self.__grid.addWidget(self.__tabs, 0, 0, 1, 1)

        self.setLayout(self.__grid)

        self.show()

