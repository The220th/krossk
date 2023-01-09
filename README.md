# krossk

Transfer encrypted msgs CROSS unsafe messengers. 

# Зависимости

Если будет использоваться функционал gpg, то нужно установить gpg.

- GNU/linux: `> sudo apt install gnupg`, `sudo pacman -S gnupg`.

- Windows: [https://gnupg.org/download/](https://gnupg.org/download/).

``` bash
> python -m ensurepip --upgrade # установка pip, если его нет

> pip3 install --upgrade pip
> pip3 install -r requirements.txt
```

# Планируемый функционал

Обмен вручную ключами шифрования.

Шифрование сообщений pycrypto:AES-256-CBC или gpg:AES-256.

Шифрование файлов pycrypto:AES-256-CBC или gpg:AES-256.

Возможно шифрование сообщений, получая ключи с помощью KDF.
