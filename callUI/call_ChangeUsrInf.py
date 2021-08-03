from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from callUI.UIWIN.ChangeUsrname import Ui_ChangeUsrname
from callUI.UIWIN.ChangePwd import Ui_ChangePwd
from callUI.call_Box import MessageBox

from userCon.user import *
from userCon.validCheck import *


class ChangeUsrname(QWidget, Ui_ChangeUsrname):
    def __init__(self, matrix, parent=None):
        super(ChangeUsrname, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()
        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix

    def setSlot(self):
        self.confirm_btn.clicked.connect(self.confirmUsrname)
        pass

    def confirmUsrname(self):
        newName = self.usrname_let.text()
        if newName == "":
            return False

        if not checkUA(newName):
            self.msgBox("警告", "用户名不合法！请更换用户名后再次尝试！")

        if hasUser(newName):
            self.msgBox("警告", "用户名已存在！请更换用户名后再次尝试！")
            return False

        usrname, pwd, uid = self.getWorkingUser()
        writeSingleLine(WORKINGUSR, ' '.join([newName, pwd, uid]))

        with open(USERLOG, 'r', encoding='utf-8') as log:
            users = log.readlines()
            for i in range(len(users)):
                if usrname in users[i].split():
                    users[i] = ' '.join([newName, pwd, uid]) + '\n'
                    break

        with open(USERLOG, 'w', encoding='utf-8') as log:
            log.writelines(users)

        self.msgBox("提示", "修改成功，请牢记您的新用户名！")

        self.matrix.welcome_lbl.setText("欢迎您，" + newName)  # self.matrix.show()
        self.close()
        pass

    @staticmethod
    def getWorkingUser():
        with open(WORKINGUSR, 'r', encoding='utf-8') as f:
            usrname, pwd, uid = f.readline().split()
        return usrname, pwd, uid

    def msgBox(self, title, text):
        message = MessageBox(self, title, text)
        message.exec()

    def showEvent(self, event):
        self.setEnabled(True)
        self.matrix.setDisabled(True)
        event.accept()

    def closeEvent(self, event):
        self.matrix.setEnabled(True)
        event.accept()


class ChangePwd(QWidget, Ui_ChangePwd):
    def __init__(self, matrix, parent=None):
        super(ChangePwd, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()
        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix

    def setSlot(self):
        self.confirm_btn.clicked.connect(self.confirmPwd)

        self.oldpwd_let.editingFinished.connect(self.checker)
        self.newpwd_let1.editingFinished.connect(self.checker)
        self.newpwd_let2.editingFinished.connect(self.checker)

        self.oldpwd_let.textEdited.connect(self.cleanOldPwdHint)
        self.newpwd_let1.textEdited.connect(self.cleanNewPwdHint1)
        self.newpwd_let2.textEdited.connect(self.cleanNewPwdHint2)

        pass

    def checker(self):
        usrname, pwd, uid = self.getWorkingUser()

        oldpwd = self.oldpwd_let.text()
        password1 = self.newpwd_let1.text()
        password2 = self.newpwd_let2.text()

        if oldpwd != pwd:
            self.errorHint(self.oldPwd_hint, "警告：原密码不正确")
            return False

        if not self.singleCheck(password1, self.newPwd_hint_1, "密码", checkPwd):
            return False

        if password1 != password2:
            self.errorHint(self.newPwd_hint_2, "警告：两次输入的密码不一致")
            return False
        return True

    def singleCheck(self, text, hint, name, method):
        if len(text) == 0:
            self.errorHint(hint, f"警告：{name}为空")
            return False
        if not method(text):
            self.errorHint(hint, f"警告：{name}不合法")
            return False
        hint.hide()
        return True

    @staticmethod
    def errorHint(hint, text):
        hint.setText(text)
        hint.setStyleSheet("color:red;")
        hint.show()

    def cleanOldPwdHint(self):
        self.oldPwd_hint.clear()

    def cleanNewPwdHint1(self):
        self.newPwd_hint_1.clear()

    def cleanNewPwdHint2(self):
        self.newPwd_hint_2.clear()

    def confirmPwd(self):
        oldpwd = self.oldpwd_let.text()
        password1 = self.newpwd_let1.text()
        password2 = self.newpwd_let2.text()

        if oldpwd == "" or password1 == "" or password2 == "":
            return False

        if not self.checker():
            return False

        usrname, pwd, uid = self.getWorkingUser()
        writeSingleLine(WORKINGUSR, ' '.join([usrname, password1, uid]))

        with open(USERLOG, 'r', encoding='utf-8') as log:
            users = log.readlines()
            for i in range(len(users)):
                if usrname in users[i].split():
                    users[i] = ' '.join([usrname, password1, uid]) + '\n'
                    break

        with open(USERLOG, 'w', encoding='utf-8') as log:
            log.writelines(users)

        self.msgBox("提示", "修改成功，请牢记您的新密码！")
        self.close()
        pass

    def msgBox(self, title, text):
        message = MessageBox(self, title, text)
        message.exec()

    @staticmethod
    def getWorkingUser():
        with open(WORKINGUSR, 'r', encoding='utf-8') as f:
            usrname, pwd, uid = f.readline().split()
        return usrname, pwd, uid

    def showEvent(self, event):
        self.setEnabled(True)
        self.matrix.setDisabled(True)
        event.accept()

    def closeEvent(self, event):

        self.oldpwd_let.clear()
        self.newpwd_let1.clear()
        self.newpwd_let2.clear()

        self.oldPwd_hint.clear()
        self.newPwd_hint_1.clear()
        self.newPwd_hint_2.clear()

        self.matrix.setEnabled(True)
        event.accept()
