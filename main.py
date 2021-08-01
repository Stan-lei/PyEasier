import sys
from PyQt5.QtWidgets import QApplication
from callUI.call_LoginWindow import LoginWindow
from path import *

if __name__ == '__main__':
    try:
        initPath()
    except FileExistsError:
        pass

    app = QApplication(sys.argv)
    loginWin = LoginWindow()
    sys.exit(app.exec_())
