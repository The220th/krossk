# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import KeyExchangeWidget, SymmetricCommunicationWidget

class MainWidget(QWidget):

    __variantsToChoose = ["Key exchange", "Symmetric communication"]

    def __init__(self):
        super().__init__()

        self.__grid = QGridLayout()

        self.__key_exchange_widget = KeyExchangeWidget(self)
        self.__symmetric_communication_widget = SymmetricCommunicationWidget(self)

        self.__stackedWidget = QStackedWidget(self)
        self.__stackedWidget.addWidget(self.__key_exchange_widget)
        self.__stackedWidget.addWidget(self.__symmetric_communication_widget)

        self.__widgetsSelectCombo = QComboBox(self)
        self.__widgetsSelectCombo.addItems(self.__variantsToChoose)
        self.__widgetsSelectCombo.activated[str].connect(self.__widgetsSelectComboActivated)

        self.__grid.addWidget(self.__widgetsSelectCombo, 0, 0, 1, 1)
        self.__grid.addWidget(self.__stackedWidget, 1, 0, 1, 1)

        self.setLayout(self.__grid)

        self.show()

    def get_SymmetricCommunicationWidget(self) -> "SymmetricCommunicationWidget":
        return self.__symmetric_communication_widget

    def __widgetsSelectComboActivated(self, text : str):
        i = 0
        for var_i in self.__variantsToChoose:
            if(text == var_i):
                break
            i-=-1
        self.__stackedWidget.setCurrentIndex(i)