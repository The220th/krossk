# -*- coding: utf-8 -*-

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QFileDialog, QStackedWidget, QTabWidget, QScrollArea)

from . import KeyExchangeWidget, SymmetricCommunicationWidget, FileTransferWidget, ico_get_question

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

class HelpWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        text = '''
<html>

<h3>Исходный код и нормальный README.md доступны тут: https://github.com/The220th/krossk</h3>

<pre>
Предположим такую ситуацию:
Алиса и Боб хотят обменяться сообщениями через мессенджер.
Причём они могут обмениваться сообщениями ТОЛЬКО через этот мессенджер (они не могут лично встретиться).
Также Алиса и Боб знают, что каждое их сообщение читает Ева.
Как Алисе и Бобу обмениваться сообщениями?
Эта программа поможет решить эту проблему.
</pre>





<h1>Вкладка Key exchange.</h1>

<pre>
Чтобы Алиса и Боб могли шифровать сообщения, им нужет "общий пароль" или passphrase.
Но passphrase нельзя написать в их мессенджер, так как Ева всё читает.
Обмен ключами возможно сделать с помощью ассиметричного шифрования. 

В krossk для этого представлены 2 алгоритма "PyCA X448" и "kRSA4096". 
    * PyCA X448 позволяет обменяться ключами с помощью Diffie-Hellman key exchange на эллиптической кривой 448. 
    * kRSA4096 - это имплементация RSA, которая тоже позволит обменяться passphrase. 

Код открыт и доступен:
* PyCA X448: https://github.com/pyca/cryptography/blob/main/src/cryptography/hazmat/primitives/asymmetric/x448.py
* kRSA4096:  https://github.com/The220th/krossk/blob/main/krossk_crypto/rsa4096.py

</pre>


<pre>
Во вкладке Key exchange происходит обмен ключами.
Участники обмена сообщениями (Алиса и Боб) делятся на 2 роли:
    * The first party;
    * The second party.

Каждый участник выбирает только 1 роль.

Обмен ключами состоит из трёх пунктов:
1. Генерация ключей участником The first party. Отправка ключей участнику The second party.
2. Получение ключей от The first party. Формирование ответа участником The second party. 
                                                                Отправка ответа участнику The first party.
3. Получение ответа от The second party и формирование общего ключа.
</pre>

<p>В программе во вкладке "Key exchange" эти пункты так и подписаны (1, 2, 3). </p>

<pre>
Пусть Алиса будет The first party, а Боб будет The second party.
Все действия Алиса делает в левой части окна, а Боб - в правой. 
</pre>

<pre>

<center>Пункт 1.</center>
Алиса нажимает кнопку Generate keys. 
Алиса копирует получившийся публичный ключ и отправляет через мессенджер Бобу.
</pre>

<pre>
<center>Пункт 2.</center>
Боб получает публичный ключ от Алисы и вставляет в окошечко с публичным ключом. 
Если используется kRSA4096, то нужно ввести генератор passphrase. В этом случае рекомендуется нажать кнопку Rnd. 
Боб нажимает кнопку под вставленным публичным ключом и полученный текст ниже отправляет Алисе через мессенджер.
Также Боб получает в нижнем правом углу этот самый "общий пароль" или passphrase.
</pre>

<pre>
<center>Пункт 3.</center>
Алиса копирует то, что прислал Боб во втором пункте и вставляет это в третьем пункте внизу. 
Далее Алиса нажимает кнопку Form key и получает в нижнем левом углу "общий пароль" или passphrase. 



</pre>

<pre>
Если всё сделано верно, то у Алисы и Боба будет одиннаковый passphrase. 
Этот одиннаковый passphrase нужно будет использовать во вкладке "Symmetric communication".
Попробуйте сначала принять на себя обе роли (The first party и The second party) и обменяться passphrase с самим собой.
</pre>

<pre>
Ева читала все сообщения, но она ничего с этим сделать не сможет (см. в гугле ассиметричное шифрование). 
Единственная адекватная возможность у Евы "взломать" сообщения - это менять ключи Алисы/Боба на свои. 
Это можно сделать только если Ева может менять сообщения в переписке в мессенджере. 
Эта уязвимость называется "человек по середине".

Грубо говоря, если Боб точно знает, что переписывается с Алисой, 
а Алиса точно знает, что переписывается с Бобом, и при этом Ева не может менять их переписку,
то "человек по середине" не страшен. 
</pre>

<pre>
Рядом с каждым полем с вводом данных/ключей/passphrase есть кнопки копировать/вставить.
Также копировать можно с помощью CTRL+C, заранее выделив весь текст с помощью комбинации клавиш CTRL+A.
Вставлять скопированный текст можно с помощью CTRL+V.
</pre>





<h1>Вкладка Symmetric communication. </h1>

<pre>
Здесь происходит шифрование сообщений. 
</pre>

<pre>
Введите passphrase, полученный во вкладке "Key exchange". Такой же passphrase должен быть и у другой стороны общения.
Сторона общения - это персона, с которой происходит обмен зашифрованными сообщениями.

Если passphrase был обговорён заранее, например, при личной встрече, то введите этот заранее обговоренный passphrase.
Главное, чтобы passphrase был одиннаковый у сторон общения.

Правее можно выбрать алгоритм симметричного шифрования. В krossk доступны 4 варианта:
    * PyCA Fernet AES128-cbc: https://github.com/pyca/cryptography/blob/main/src/cryptography/fernet.py
    * GPG AES256:  https://dev.gnupg.org/source/gnupg/
    * GPG default: https://dev.gnupg.org/source/gnupg/
    * kaes256CBC: https://github.com/The220th/py_AES256_cbc_implementation/blob/main/kaes256cipher.py

* Fernet - это спецификация: https://github.com/fernet/spec/ 
* GPG AES256 и GPG default отличаются только параметром "--s2k-cipher-algo". 
              В "GPG AES256" он равен "AES256", а в "GPG default" он пустой.

Ещё правее можно будет посмотреть логи ("переписку"). Для этого нажмите кнопку "Veiw logs". 
Если ни одного сообщения ещё не было зашифровано/расшифровано, то логи ("переписка") будут пустые. 
Все логи удаляются после закрытия программы. Поэтому сохранять их, если это необходимо, нужно будет вручную.
</pre>
 
<pre>
Чтобы зашифровать сообщение другой стороне, напишите сообщение в большом окошке слева, нажмите кнопку Encrypt.
Ниже кнопки Encrypt появятся символы, их нужно отправить другой стороне через мессенджер. 
Чтобы скопировать символы нажмите кнопку копирования правее или испольнуйте CTRL+A, CTRL+C.
</pre>

<pre>
После того, как получите зашифрованные символы от другой стороны общения, скопируйте их 
и вставьте ниже надписи "Enter message from the other party" в окошко сверху справа.
Чтобы вставить используйте CTRL+V или нажмите кнопку вставки правее окошка.
Далее нажмите кнопку Decrypt. Ниже в большом окошке справа появится расшифрованной сообщение от первой стороны.
</pre>

<p>Никто не запрещает шифровать сообщения последовательно разными алгоритмами симметричного шифрования.</p>

<pre>
Чтобы посмотреть все зашифрованные и расшифрованные сообщения или же логи ("переписка") используйте кнопку "Veiw logs".

Выше кнопки "Veiw logs" есть кнопка "Add new communication" для добавления новой среды. 
Переключаться между ними можно с помощью выпадающего списка левее кнопки "Add new communication".
В каждой новой среде можно выставить разные алгоритмы симметричного шифрования. 
Также в каждой новой среде будут свои логи ("переписка").
Каждая новая среда нужна для кажной новой стороны общения. 
</pre>

<p>Для тренировки можете принять на себя роль всех сторон общения и шифровать/расшифровывать свои же сообщение самому себе. </p>





<h1>Вкладка Encrypt/decrypt file. </h1>

<pre>
Здесь происходит шифрование файлов.
</pre>

<pre>
Введите passphrase. Это пароль с помощью которого потом можно будет расшифровать этот файл.

Выбирите алгоритм шифрования. В krossk доступны 4 варианта:
    * PyCA Fernet AES128-cbc: https://github.com/pyca/cryptography/blob/main/src/cryptography/fernet.py
    * GPG AES256:  https://dev.gnupg.org/source/gnupg/
    * GPG default: https://dev.gnupg.org/source/gnupg/
    * kaes256CBC: https://github.com/The220th/py_AES256_cbc_implementation/blob/main/kaes256cipher.py

* Fernet - это спецификация: https://github.com/fernet/spec/ 
* GPG AES256 и GPG default отличаются только параметром "--s2k-cipher-algo". 
              В "GPG AES256" он равен "AES256", а в "GPG default" он пустой.
* kaes256CBC будет работать очень медленно. Шифруйте им небольшие файлы. 

После выбора файла для шифрования (и места его сохранения) нажмите кнопку Encrypt или Decrypt. 
</pre>

<p>Теперь зашифрованный файл можно отправить в небезопасном мессенджере. </p>

<p>Никто не запрещает шифровать сначала одним алгоритмом, а потом другим, меняя passphrase. </p>

<pre>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n</pre>
</html>
'''
        self.__help_label = QLabel(text, self)
        self.__help_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.__help_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.__scroll = QScrollArea(self)
        self.__scroll.setWidgetResizable(True)
        self.__scroll.setWidget(self.__help_label)

        self.__grid.addWidget(self.__scroll, 0, 0, 1, 1)
        
        self.setLayout(self.__grid)
