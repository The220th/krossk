# -*- coding: utf-8 -*- 

from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QLabel, QCheckBox, QTextEdit, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QGridLayout, QComboBox, QRadioButton, QFileDialog, QStackedWidget, QTabWidget, QScrollArea)

class HelpWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__grid = QGridLayout()

        text = self.get_ru_help_text()

        self.__help_label = QLabel(text, self)
        self.__help_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.__help_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.__scroll = QScrollArea(self)
        self.__scroll.setWidgetResizable(True)
        self.__scroll.setWidget(self.__help_label)

        self.__ru_radio_button = QRadioButton("Русский")
        self.__ru_radio_button.setChecked(True)
        self.__ru_radio_button.toggled.connect(lambda: self.__radio_button_handler(1))

        self.__en_radio_button = QRadioButton("English")
        self.__en_radio_button.toggled.connect(lambda: self.__radio_button_handler(0))

        self.__grid.addWidget(self.__ru_radio_button, 0, 0, 1, 1)
        self.__grid.addWidget(self.__en_radio_button, 0, 1, 1, 1)
        self.__grid.addWidget(self.__scroll, 1, 0, 1, 2)
        
        self.setLayout(self.__grid)

    def __radio_button_handler(self, lang: int):
        #radioButton = self.sender()
        if(lang == 0):
            text = self.get_en_help_text()
        elif(lang == 1):
            text = self.get_ru_help_text()
        else:
            text = "Failed successfully. "
        self.__help_label.setText(text)

    def get_ru_help_text(self) -> str:
        text = '''
<html>

<h3>Исходный код и полный README.md доступны тут: https://github.com/The220th/krossk</h3>

<p>Нужно сказать, что использование программы на свой страх и риск.</p>

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
Чтобы Алиса и Боб могли шифровать сообщения, им нужен "общий пароль" или passphrase.
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
Если используется kRSA4096, то нужно ввести генератор passphrase. В этом случае рекомендуется нажать кнопку "Rnd". 
Боб нажимает кнопку под вставленным публичным ключом и полученный текст ниже отправляет Алисе через мессенджер.
Также Боб получает в нижнем правом углу этот самый "общий пароль" или passphrase.
</pre>

<pre>
<center>Пункт 3.</center>
Алиса копирует то, что прислал Боб во втором пункте и вставляет это в третьем пункте внизу. 
Далее Алиса нажимает кнопку Form key и получает в нижнем левом углу "общий пароль" или passphrase. 



</pre>

<pre>
Если всё сделано верно, то у Алисы и Боба будет одинаковый passphrase. 
Этот одинаковый passphrase нужно будет использовать во вкладке "Symmetric communication".
Попробуйте сначала принять на себя обе роли (The first party и The second party) и обменяться passphrase с самим собой.
</pre>

<pre>
Ева читала все сообщения, но она ничего с этим сделать не сможет (см. в гугле ассиметричное шифрование). 
Математика ей не позволит.
Единственная адекватная возможность у Евы "взломать" сообщения - это менять ключи Алисы/Боба на свои. 
Это можно сделать только если Ева может менять сообщения в переписке в мессенджере. 
Эта уязвимость называется "человек посередине".

Грубо говоря, если Боб точно знает, что переписывается с Алисой, 
а Алиса точно знает, что переписывается с Бобом, и при этом Ева не может менять их переписку,
то "человек посередине" не страшен. 
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
Главное, чтобы passphrase был одинаковый у сторон общения.

Правее можно выбрать алгоритм симметричного шифрования. В krossk доступны 4 варианта:
    * PyCA Fernet AES128-cbc: https://github.com/pyca/cryptography/blob/main/src/cryptography/fernet.py
    * GPG AES256:  https://dev.gnupg.org/source/gnupg/
    * GPG default: https://dev.gnupg.org/source/gnupg/
    * kaes256CBC: https://github.com/The220th/py_AES256_cbc_implementation/blob/main/kaes256cipher.py

* Fernet - это спецификация: https://github.com/fernet/spec/ 
* "GPG AES256" и "GPG default" отличаются только параметром "--s2k-cipher-algo". 
              В "GPG AES256" он равен "AES256", а в "GPG default" он пустой.
Программу "GPG" нужно установить отдельно. 
На Windows могут наблюдаться проблемы, связанные с кодировкой. 

Ещё правее можно будет посмотреть логи ("переписку"). Для этого нажмите кнопку "View logs". 
Если ни одного сообщения ещё не было зашифровано/расшифровано, то логи ("переписка") будут пустые. 
Все логи удаляются после закрытия программы. Поэтому сохранять их, если это необходимо, нужно будет вручную.
</pre>
 
<pre>
Чтобы зашифровать сообщение другой стороне, напишите сообщение в большом окошке слева и нажмите кнопку Encrypt.
Ниже кнопки Encrypt появятся символы (зашифрованное сообщение), их нужно отправить другой стороне через мессенджер. 
Чтобы скопировать символы, нажмите кнопку копирования правее или используйте CTRL+A, CTRL+C.
Максимальная длина выходного сообщения 32767 символов. 
Слишком длинные сообщения шифруйте как файлы во вкладке "Encrypt/decrypt file".
</pre>

<pre>
После того как получите зашифрованные символы от другой стороны общения, скопируйте их 
и вставьте в текстовое поле "Enter message from the other party" в окошко сверху справа.
Чтобы вставить, используйте CTRL+V или нажмите кнопку вставки правее окошка.
Далее нажмите кнопку Decrypt. Ниже в большом окошке справа появится расшифрованной сообщение от первой стороны.
</pre>

<p>Никто не запрещает шифровать сообщения последовательно разными алгоритмами симметричного шифрования.</p>

<pre>
Чтобы посмотреть все зашифрованные и расшифрованные сообщения или же логи ("переписка"), используйте кнопку "Veiw logs".

Выше кнопки "View logs" есть кнопка "Add new communication" для добавления новой среды. 
Переключаться между ними можно с помощью выпадающего списка левее кнопки "Add new communication".
В каждой новой среде можно выставить разные алгоритмы симметричного шифрования. 
Также в каждой новой среде будут свои логи ("переписка").
Каждая новая среда нужна для каждой новой стороны общения. 
</pre>

<p>Для тренировки можете принять на себя роль всех сторон общения и шифровать/расшифровывать свои же сообщение самому себе. </p>





<h1>Вкладка Encrypt/decrypt file. </h1>

<pre>
Здесь происходит шифрование файлов.
</pre>

<pre>
Введите passphrase. Это пароль с помощью которого потом можно будет расшифровать этот файл.
Им он и шифруется. 

Выберите алгоритм шифрования. В krossk доступны 4 варианта:
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
        return text

    def get_en_help_text(self) -> str:
        text = '''
<html>

<h3>Source code and full README.md available here: https://github.com/The220th/krossk</h3>

<p>Must say that the use of the program is at your own risk.</p>

<pre>
Example:
Alice and Bob want to exchange messages using some messenger.
Moreover, they can exchange messages ONLY through this messenger (they cannot meet in person).
Alice and Bob also know that Eve reads their every message.
How can Alice and Bob exchange messages so that Eve can't read them?
This program will help solve this problem.
</pre>





<h1>Key exchange tab.</h1>

<pre>
In order for Alice and Bob to encrypt messages, they need a "shared password" or passphrase.
But passphrase cannot be written to their messenger, since Eva reads everything.
Key exchange can be done using asymmetric encryption.

In krossk, 2 algorithms "PyCA X448" and "kRSA4096" are presented for this.
    * PyCA X448 allows you to exchange keys using Diffie-Hellman key exchange method on an elliptical curve 448.
    * kRSA4096 is an implementation of RSA, which will also allow you to exchange passphrase.

The code is open-source and available at:
* PyCA X448: https://github.com/pyca/cryptography/blob/main/src/cryptography/hazmat/primitives/asymmetric/x448.py
* kRSA4096:  https://github.com/The220th/krossk/blob/main/krossk_crypto/rsa4096.py

</pre>


<pre>
You can exchange keys on the "Key Exchange" tab
The messaging participants (Alice and Bob) are divided into 2 roles:
    * The first party;
    * The second party.

Each participant chooses only 1 role.

The key exchange consists of three points:
1. Key generation by the participant of The first party. Sending keys to the participant of The second party.
2. Getting the keys from The first party. Forming a response by a participant of The second party.
                                                                Sending a response to the participant of The first party.
3. Receiving a response from The second party and forming a shared key.
</pre>

<p>In the program, in the "Key exchange" tab, these items are signed as (1, 2, 3). </p>

<pre>
Let Alice be The first party and Bob be The second party.
Alice does all the actions on the left side of the window, and Bob does them on the right.
</pre>

<pre>

<center>Step 1.</center>
Alice presses the "Generate keys" button.
Alice copies the created public key and sends it to Bob via messenger.
</pre>

<pre>
<center>Step 2.</center>
Bob receives the public key from Alice and inserts it into the "Public key" text field.
If kRSA4096 is used, then you need to enter the passphrase generator. In such case, you can press the "Rnd" button to make a random one.
Bob presses the button under the public key and sends the received text below to Alice via messenger.
Bob also receives the "common password" or passphrase in the lower right corner.
</pre>

<pre>
<center>Step 3.</center>
Alice copies what Bob sent in the second paragraph and inserts it in the third step at the bottom.
Next, Alice presses the Form key button and receives a "common password" or passphrase in the lower left corner.



</pre>

<pre>
If everything is done correctly, then Alice and Bob will have the same passphrase.
This identical passphrase will need to be used in the "Symmetric communication" tab.
Try to assume both roles first (The first party and The second party) and exchange passphrase with yourself.
</pre>

<pre>
Eva has read all the messages, but she can't do anything about it (due to asymmetric encryption).
The only way for Eve to "hack" the messages is to change Alice's/Bob's keys to her own.
This can only be done if Eva can change the messages in the correspondence in the messenger.
Such vulnerability is called "man in the middle".

Roughly speaking, if Bob knows for sure that he is texting with Alice,
and Alice knows for sure that she is texting with Bob, and at the same time Eve cannot change their correspondence,
then the "man in the middle" is not to be feared of.
</pre>

<pre>
There are copy/paste buttons next to each data/key/passphrase entry field.
You can also copy using CTRL+C, pre-selecting the entire text using the CTRL+A keyboard shortcut.
You can paste the copied text using CTRL+V.
</pre>





<h1>The Symmetrical communication tab. </h1>

<pre>
This is where message encryption takes place.
</pre>

<pre>
Enter the passphrase received in the "Key exchange" tab. The other side of the communication should have the same passphrase.
The communication side meaning the person with whom encrypted messages are exchanged.

If the passphrase was negotiated in advance, for example, during a personal meeting, then enter this pre-negotiated passphrase.
It is important that the passphrase is the same for both communication parties.

In the window on the top right, in the drop-down menu, you can select the symmetric encryption algorithm. There are 4 options available:
    * PyCA Fernet AES128-cbc: https://github.com/pyca/cryptography/blob/main/src/cryptography/fernet.py
    * GPG AES256:  https://dev.gnupg.org/source/gnupg/
    * GPG Default: https://dev.gnupg.org/source/gnupg/
    * kaes256CBC: https://github.com/The220th/py_AES256_cbc_implementation/blob/main/kaes256cipher.py

* Fernet: https://github.com/fernet/spec/
* "GPG AES256" and "GPG default" differ only in the parameter "--s2k-cipher-algo".
              In "GPG AES256" it is equal to "AES256", and in "GPG default" it is empty.
"GPG" needs to be installed separately. There may be encoding issues on Windows.

The "View logs" button allows you to see the history of encrypted/decrypted messages.
If no messages have been encrypted/decrypted yet, the logs ("correspondence") will be empty.
All data is deleted after the program is closed. Therefore, you will need to save it manually if necessary.
</pre>

<pre>
To encrypt a message to the other party, write a message in the large text field on the left and click the Encrypt button.
The encrypted string will appear below the Encrypt button, which you need to send to the other party via messenger.
To copy the characters, press the copy button to the right or use CTRL+A, CTRL+C.
</pre>

<pre>
After you receive the encrypted string from the other party, copy them
and paste in the text field "Enter message from the other party" on the right side of the window.
To paste, use CTRL+V or click the paste button to the right of the window.
Next, click Decrypt. Now, the decrypted message from the first party will appear in the large text field below.
</pre>

<p>You can encrypt messages sequentially with different symmetric encryption algorithms.</p>

<pre>
To view all encrypted and decrypted messages or logs ("correspondence"), use the "View logs" button.

Above the "View logs" button, there is an "Add new communication" button to add a new environment.
You can switch between them using the drop-down list to the left of the "Add new communication" button.
In each new environment, you can set different symmetric encryption algorithms.
Also, each new environment will have its own logs ("correspondence").
Every new environment is needed for every new side of communication.
</pre>

<p>For training, you can take on the role of all sides of communication and encrypt/decrypt your own message to yourself. </p>





<h1>The Encrypt/decrypt file tab. </h1>

<pre>
This is where file encryption takes place.
</pre>

<pre>
Enter passphrase. This is the password with which you can encrypt and decrypt the file.

Select the encryption algorithm. There are 4 options available in krossk:
    * PyCA Fernet AES128-cbc: https://github.com/pyca/cryptography/blob/main/src/cryptography/fernet.py
    * GPG AES256:  https://dev.gnupg.org/source/gnupg/
    * GPG default: https://dev.gnupg.org/source/gnupg/
    * kaes256CBC: https://github.com/The220th/py_AES256_cbc_implementation/blob/main/kaes256cipher.py

* Fernet: https://github.com/fernet/spec/
* GPG AES256 and GPG default differ only in the parameter "--s2k-cipher-algo".
              In "GPG AES256" it is equal to "AES256", and in "GPG default" it is empty.
* kaes256CBC will run very slowly. Encrypt small files with it.

After selecting the file to encrypt (and where to save it), click the Encrypt or Decrypt button.
</pre>

<p>Now the encrypted file can be sent in an insecure messenger. </p>

<p>You can also encrypt using multiple encryption algorithms, changing the passphrase between them. </p>

<pre>\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n</pre>
</html>
'''
        return text

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWidget = HelpWidget(None)
    mainWidget.show()
    sys.exit(app.exec_())