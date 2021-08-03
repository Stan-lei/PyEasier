from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget
from callUI.UIWIN.UserCenter import Ui_UserCenter
from callUI.call_ChangeUsrInf import ChangeUsrname, ChangePwd

from path import *


class UserCenter(QWidget, Ui_UserCenter):
    def __init__(self, matrix, parent=None):
        super(UserCenter, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()

        self.matrix = matrix

        self.avatar_lbl.setPixmap(QPixmap(PICSRC + "avatar.jpg"))
        self.avatar_lbl.setScaledContents(True)
        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.changeUsrname = ChangeUsrname(self)
        self.changePwd = ChangePwd(self)

    def setSlot(self):
        self.changeUname_btn.clicked.connect(self.call_changeUsrname)
        self.changePwd_btn.clicked.connect(self.call_changePwd)
        pass

    def call_changeUsrname(self):
        self.changeUsrname.show()
        pass

    def call_changePwd(self):
        self.changePwd.show()
        pass

    @staticmethod
    def getWorkingUser():
        with open(WORKINGUSR, 'r', encoding='utf-8') as f:
            usrname, pwd, uid = f.readline().split()
        return usrname, pwd, uid

    def showEvent(self, event):
        self.setEnabled(True)
        self.matrix.setDisabled(True)
        usrname, pwd, uid = self.getWorkingUser()
        self.welcome_lbl.setText("欢迎您，" + usrname)
        event.accept()

    def closeEvent(self, event):
        self.changeUsrname.close()
        self.changePwd.close()
        self.matrix.setEnabled(True)
        event.accept()
