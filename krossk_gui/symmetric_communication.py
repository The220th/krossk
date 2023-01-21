# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QVBoxLayout, QComboBox, QFileDialog, QStackedWidget, QGroupBox)

from . import ifMsg, exe_widget_in_QDialog, PasswordWidget, HiddenLineEditWidget, CopyPasteEditWidget
from . import ico_get_chat, ico_get_chat_in, ico_get_chat_out

from krossk_crypto import Pyca_Fernet, gpg_cipher, kaes256CBC, check_passphrase_is_strong

class SymmetricCommunicationWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__add_new_communication_widget = AddNewCommunicationWidget(self)

        self.__grid = QGridLayout()

        self.__addNewCommunication_button = QPushButton("Add new communication", self)
        self.__addNewCommunication_button.clicked.connect(lambda:self.__addNewCommunication_button_handler())

        self.__list_of_communications = ["communication 0"]
        self.__list_of_communications_widgets = [OneSymmetricCommunicationWidget(self, self.__list_of_communications[0])]
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
            ifMsg(self, f"\"{communication_name}\" already exists. Choose another communication name", 4)
            return
        self.__list_of_communications.append(communication_name)
        communication_widget = OneSymmetricCommunicationWidget(self, communication_name)
        self.__list_of_communications_widgets.append(communication_widget)
        self.__stackedWidget.addWidget(communication_widget)
        self.__widgetsSelectCombo.addItem(communication_name)


    def check_if_communication_exists(self, communication_name: str):
        if(communication_name in self.__list_of_communications):
            return True
        else:
            return False
        


class OneSymmetricCommunicationWidget(QWidget):

    __ciphers_list = ["PyCA Fernet AES128-cbc", "gpg AES256", "kaes256CBC"] # порядок не менять! 

    def __init__(self, parent, communication_name: str):
        super().__init__(parent)
        self.__communication_name = communication_name

        self.__grid = QGridLayout()
        
        self.__pswd = PasswordWidget(self, "Passphrase:")

        self.__ciphers_combo = QComboBox(self)
        self.__ciphers_combo.addItems(self.__ciphers_list)
        self.__ciphers_combo.activated[str].connect(self.__ciphers_combo_handler)
        self.__ciphers_combo_prev_index = 0

        self.__chat_messages = []
        self.__veiw_chat_button = QPushButton(ico_get_chat(), "View logs", self)
        self.__veiw_chat_button.clicked.connect(lambda: self.__veiw_chat_button_handler())
        
        self.__grid.addWidget(self.__pswd, 0, 0, 1, 1)
        self.__grid.addWidget(QLabel("Select cipher:", self), 0, 1, 1, 1)
        self.__grid.addWidget(self.__ciphers_combo, 0, 2, 1, 1)
        self.__grid.addWidget(self.__veiw_chat_button, 0, 3, 1, 1)

        self.__chat_out = QTextEdit(self)
        self.__chat_out.setReadOnly(False)
        self.__chat_out.setMinimumSize(QtCore.QSize(350, 350))
        self.__chat_encrypt_button = QPushButton(ico_get_chat_out(), "Encrypt", self)
        self.__chat_encrypt_button.clicked.connect(lambda: self.__chat_encrypt_button_handler())
        self.__chat_out_en = CopyPasteEditWidget(self, True, False)

        self.__chat_in = QTextEdit(self)
        self.__chat_in.setReadOnly(True)
        self.__chat_in.setMinimumSize(QtCore.QSize(350, 350))
        self.__chat_decrypt_button = QPushButton(ico_get_chat_in(), "Decrypt", self)
        self.__chat_decrypt_button.clicked.connect(lambda: self.__chat_decrypt_button_handler())
        self.__chat_in_en = CopyPasteEditWidget(self, False, True)

        # ========== up-down, down-up ==========
        self.__gb1 = QGroupBox("", self)
        self.__gb2 = QGroupBox("", self)
        gb1_l = QVBoxLayout(self.__gb1)
        gb2_l = QVBoxLayout(self.__gb2)
        self.__gb1.setLayout(gb1_l)
        self.__gb2.setLayout(gb2_l)

        gb1_l.addWidget(QLabel("Type message to the other party:", self))
        gb1_l.addWidget(self.__chat_out)
        gb1_l.addWidget(self.__chat_encrypt_button)
        gb1_l.addWidget(QLabel("Send this encrypted message to the other party:"))
        gb1_l.addWidget(self.__chat_out_en)
        
        self.__grid.addWidget(self.__gb1, 1, 0, 1, 2)

        #self.__grid.addWidget(QLabel("Type message to the other party:", self), 1, 0, 1, 2)
        #self.__grid.addWidget(self.__chat_out, 2, 0, 1, 2)
        #self.__grid.addWidget(self.__chat_encrypt_button, 3, 0, 1, 2)
        #self.__grid.addWidget(QLabel("Send this encrypted message to the other party:", self), 4, 0, 1, 2)
        #self.__grid.addWidget(self.__chat_out_en, 5, 0, 1, 2)

        gb2_l.addWidget(QLabel("Enter message from the other party:", self))
        gb2_l.addWidget(self.__chat_in_en)
        gb2_l.addWidget(self.__chat_decrypt_button)
        gb2_l.addWidget(QLabel("Decrypted message from the other party:"))
        gb2_l.addWidget(self.__chat_in)

        self.__grid.addWidget(self.__gb2, 1, 2, 1, 2)

        #self.__grid.addWidget(QLabel("Decrypted message from the other party:", self), 1, 2, 1, 2)
        #self.__grid.addWidget(self.__chat_in, 2, 2, 1, 2)
        #self.__grid.addWidget(self.__chat_decrypt_button, 3, 2, 1, 2)
        #self.__grid.addWidget(QLabel("Enter message from the other party:", self), 4, 2, 1, 2)
        #self.__grid.addWidget(self.__chat_in_en, 5, 2, 1, 2)

        self.setLayout(self.__grid)

    def __ciphers_combo_handler(self, text: str):
        if(text == self.__ciphers_list[1]):
            gpg_cipher_test = gpg_cipher("123")
            if(gpg_cipher_test.check_gpg_insystem_exists() == False):
                ifMsg(self, "gpg is not installed! ", 4)
                self.__ciphers_combo.setCurrentIndex(self.__ciphers_combo_prev_index)
                return

        self.__ciphers_combo_prev_index = self.__ciphers_combo.currentIndex()

    def __chat_encrypt_button_handler(self):
        msg_src = self.__chat_out.toPlainText()
        if(msg_src == ""):
            ifMsg(self, "Your message is empty. Fill it first. ", 4)
            return

        cipher_key = self.__pswd.get_password()
        if(cipher_key == ""):
            ifMsg(self, "Fill passphrase", 4)
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
            cipher = gpg_cipher(cipher_key)
        elif(cipher_combo_text == self.__ciphers_list[2]):
            cipher = kaes256CBC(cipher_key)
        else:
            ifMsg(self, "Failed successfully. ", 4)
            return
        
        try:
            msg_src_en = cipher.encrypt_msg(msg_src)
            if(msg_src_en == None):
                ifMsg(self, "Cannot encrypt! Invalid passphrase or cipher? ", 4)
        except:
            import traceback
            print(traceback.format_exc())
            ifMsg(self, "Cannot encrypt! ", 4)
            return

        self.__chat_out_en.setText(msg_src_en)
        self.__chat_messages.append(f"[you] {msg_src}")

    def __chat_decrypt_button_handler(self):
        msg_en_src = self.__chat_in_en.text()
        if(msg_en_src == ""):
            ifMsg(self, "Message from the other party is empty. Fill it first. ", 4)
            return

        cipher_key = self.__pswd.get_password()
        if(cipher_key == ""):
            ifMsg(self, "Fill passphrase", 4)
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
            cipher = gpg_cipher(cipher_key)
        elif(cipher_combo_text == self.__ciphers_list[2]):
            cipher = kaes256CBC(cipher_key)
        else:
            ifMsg(self, "Failed successfully. ", 4)
            return

        try:
            msg_src = cipher.decrypt_msg(msg_en_src)
            if(msg_src == None):
                ifMsg(self, "Cannot decrypt! Invalid passphrase, cipher or encrypted text? ", 4)
        except:
            import traceback
            print(traceback.format_exc())
            ifMsg(self, "Cannot decrypt! ", 4)
            return

        self.__chat_in.setText(msg_src)
        self.__chat_messages.append(f"[the other party] {msg_src}")

    def __veiw_chat_button_handler(self):
        show_chat_widget = QWidget(self)
        grid = QGridLayout()
        grid.addWidget(QLabel(f"\"{self.__communication_name}\" logs: ", self), 0, 0, 1, 1)
        chat_text = QTextEdit(self)
        chat_text.setReadOnly(True)
        for msg in self.__chat_messages:
            chat_text.append(msg)
        chat_text.setMinimumSize(QtCore.QSize(500, 500))

        grid.addWidget(chat_text, 1, 0, 1, 1)

        show_chat_widget.setLayout(grid)
    
        exe_widget_in_QDialog(self, show_chat_widget)



class AddNewCommunicationWidget(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent

        self.__grid = QGridLayout()

        self.__text_input = QLineEdit(self)
        self.__text_input.setReadOnly(False)
        self.__text_input.textChanged.connect(lambda: self.__text_input_handler())

        self.__add_button = QPushButton("Add", self)
        self.__add_button.clicked.connect(lambda: self.__add_button_handler())
        #self.__add_button.setDefault(True)
        #self.__add_button.setFocus()

        self.__status_label = QLabel("", self)

        self.__grid.addWidget(QLabel("Enter new communication name: ", self), 0, 0, 1, 1)
        self.__grid.addWidget(self.__text_input, 1, 0, 1, 1)
        self.__grid.addWidget(self.__add_button, 2, 0, 1, 1)
        self.__grid.addWidget(QLabel("If you need to add multiple new communication, \nseparate them by comma (\",\")."), 3, 0, 1, 1)
        self.__grid.addWidget(self.__status_label, 4, 0, 1, 1)

        self.setLayout(self.__grid)
    
    def __add_button_handler(self):
        self.__status_label.setText("")
        new_com_name = self.__text_input.text()
        if(new_com_name == ""):
            ifMsg(self, "Fill communication name", 4)
            return
        
        if(new_com_name.find(",") != -1):
            new_com_names = list(new_com_name.split(","))
            for new_com_name_i in new_com_names:
                new_com_name_i = new_com_name_i.strip()
                if(self.__parent.check_if_communication_exists(new_com_name_i)):
                    ifMsg(self, f"\"{new_com_name_i}\" already exists. Choose another communication name", 4)
                    return
            for new_com_name_i in new_com_names:
                self.__parent.addNewCommunication(new_com_name_i)
            self.__status_label.setText("Added!")
        else:
            new_com_name = new_com_name.strip()
            if(self.__parent.check_if_communication_exists(new_com_name)):
                ifMsg(self, f"\"{new_com_name}\" already exists. Choose another communication name", 4)
                return
            self.__parent.addNewCommunication(new_com_name)
            self.__status_label.setText("Added!")

    def __text_input_handler(self):
        self.__status_label.setText("")
