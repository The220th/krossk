# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from krossk_gui import MainWidget, ico_get_main



if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWidget = MainWidget()
    mainWidget.setWindowTitle("filecryptodisk")

    mainWidget.setWindowIcon(ico_get_main())

    sys.exit(app.exec_())