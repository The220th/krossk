# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from krossk_gui import MainWidget, ico_get_main


KROSSK_VERSION = "V0.77"

def flags_react(args: list):
    argc = len(args)
    if(argc >= 2 and args[1] == "--version"):
        print(KROSSK_VERSION)
        exit()
    if(argc >= 2 and args[1] == "--help"):
        print("See README.md: https://github.com/The220th/krossk")
        exit()

if __name__ == '__main__':
    flags_react(sys.argv)

    app = QApplication(sys.argv)

    mainWidget = MainWidget()
    mainWidget.setWindowTitle("filecryptodisk")

    mainWidget.setWindowIcon(ico_get_main())

    sys.exit(app.exec_())