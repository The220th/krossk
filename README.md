# krossk

Transfer encrypted msgs CROSS unsafe messengers. 

# Зависимости

Если будет использоваться функционал gpg, то нужно установить gpg.

- GNU/linux: `> sudo apt install gnupg`, `sudo pacman -S gnupg`.

- Windows: [https://gnupg.org/download/](https://gnupg.org/download/).

``` bash
> python -m ensurepip --upgrade # установка pip, если его нет

> pip install --upgrade pip
> pip install -r requirements.txt
```

# Компиляция одного исполняемого файла

``` bash
> git clone https://github.com/The220th/krossk
> cd krossk
> python -m venv new_venv

> source ./new_venv/bin/activate  # GNU/Linux
> .\new_venv\Scripts\activate.bat # Windows

> pip freeze > requirements_for_delete.txt
> pip uninstall -r requirements_for_delete.txt -y

> pip install --upgrade pip
> pip install -r requirements.txt
> pip install pyinstaller

> pyinstaller --onefile --paths=new_venv/lib64/python3.10/site-packages/:new_venv/lib/python3.10/site-packages/ krossk.py # GNU/Linux
> pyinstaller --onefile --paths=new_venv\Lib\site-packages --windowed krossk.py # Windows

# В директории dist будет лежать исполняемый файл
```

# Запуск

Либо скачайте исполняемый файл из [релизов https://github.com/The220th/krossk/releases](https://github.com/The220th/krossk/releases) и запустите его. 

Либо:

``` bash
> git clone https://github.com/The220th/krossk
> cd krossk
> python krossk.py
```