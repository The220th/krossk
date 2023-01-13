# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget)

from . import ifMsg, exe_widget_in_QDialog, PasswordWidget, HiddenLineEditWidget

class SymmetricCommunicationWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__add_new_communication_widget = AddNewCommunicationWidget(self)

        self.__grid = QGridLayout()

        self.__addNewCommunication_button = QPushButton("Add new communication", self)
        self.__addNewCommunication_button.clicked.connect(lambda:self.__addNewCommunication_button_handler())

        self.__list_of_communications = ["communication 0"]
        self.__list_of_communications_widgets = [OneSymmetricCommunicationWidget(self)]
        self.__stackedWidget = QStackedWidget(self)
        self.__stackedWidget.addWidget(self.__list_of_communications_widgets[0])

        self.__widgetsSelectCombo = QComboBox(self)
        self.__widgetsSelectCombo.addItems(self.__list_of_communications)
        self.__widgetsSelectCombo.activated[str].connect(self.__widgetsSelectComboActivated)
        
        self.__grid.addWidget(self.__widgetsSelectCombo, 0, 0, 1, 1)
        self.__grid.addWidget(self.__addNewCommunication_button, 0, 1, 1, 1)
        self.__grid.addWidget(self.__stackedWidget, 1, 0, 1, 2)

        self.setLayout(self.__grid)

    def __widgetsSelectComboActivated(self, text: str):
        i = 0
        for var_i in self.__list_of_communications:
            if(text == var_i):
                break
            i-=-1
        self.__stackedWidget.setCurrentIndex(i)

    def __addNewCommunication_button_handler(self):
        exe_widget_in_QDialog(self, self.__add_new_communication_widget)

    def addNewCommunication(self, communication_name: str):
        if(self.check_if_communication_exists(communication_name)):
            ifMsg(self, f"\"{new_com_name}\" already exists. Choose another communication name", 4)
            return
        self.__list_of_communications.append(communication_name)
        communication_widget = OneSymmetricCommunicationWidget(self)
        self.__list_of_communications_widgets.append(communication_widget)
        self.__stackedWidget.addWidget(communication_widget)
        self.__widgetsSelectCombo.addItem(communication_name)


    def check_if_communication_exists(self, communication_name: str):
        if(communication_name in self.__list_of_communications):
            return True
        else:
            return False
        

class OneSymmetricCommunicationWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()
        import random
        self.__grid.addWidget(QLabel(f"{random.randint(0, 100)}", self), 0, 0, 1, 1)

        self.setLayout(self.__grid)

class AddNewCommunicationWidget(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent

        self.__grid = QGridLayout()

        self.__text_input = QLineEdit(self)
        self.__text_input.setReadOnly(False)

        self.__add_button = QPushButton("Add", self)
        self.__add_button.clicked.connect(lambda: self.__add_button_handler())

        self.__grid.addWidget(QLabel("Enter new communication name: ", self), 0, 0, 1, 1)
        self.__grid.addWidget(self.__text_input, 1, 0, 1, 1)
        self.__grid.addWidget(self.__add_button, 2, 0, 1, 1)

        self.setLayout(self.__grid)
    
    def __add_button_handler(self):
        new_com_name = self.__text_input.text()
        if(new_com_name == ""):
            ifMsg(self, "Fill communication name", 4)
            return
        if(self.__parent.check_if_communication_exists(new_com_name)):
            ifMsg(self, f"\"{new_com_name}\" already exists. Choose another communication name", 4)
            return
        self.__parent.addNewCommunication(new_com_name)

