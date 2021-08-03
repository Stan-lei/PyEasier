from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, qApp, QWidget
from callUI.UIWIN.LoginWindow import Ui_LoginWindow
from callUI.UIWIN.RegisterForm import Ui_RegisterForm
from callUI.UIWIN.CleanPwd import Ui_CleanPwd
from callUI.call_Box import *
from callUI.call_WorkingWin import WorkingWindow
from userCon.user import *
from userCon.validCheck import *


class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.registerForm = RegisterForm()

        self.logo_lbl.setPixmap(QPixmap(PICSRC + "logo.png"))
        self.logo_lbl.setScaledContents(True)

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.workingWindow = WorkingWindow(self)
        self.pwdCleaner = CleanPwd(self)
        self.setSlot()
        self.show()

    def setSlot(self):
        self.actionExit.triggered.connect(qApp.quit)
        self.actioncleanPwd.triggered.connect(self.cleanPwd)
        self.login_btn.clicked.connect(self.tryLogin)
        self.register_btn.clicked.connect(self.callRegister)
        pass

    def tryLogin(self):
        username = self.usr_let.text()
        password = self.pwd_let.text()
        if username == "" or password == "":
            return False

        usrInf = getUser(username)
        if usrInf is None:
            self.msgBox("警告", "用户不存在，请注册后再进行登录！")
            return False

        usr, pwd, uid = usrInf.split()
        if password != pwd:
            self.msgBox("警告", "密码错误，请再次尝试！")
            return False

        self.msgBox("提示", "登录成功！请享受做题的乐趣吧！")

        writeSingleLine(WORKINGUSR, usrInf)
        self.callWorkingWin()
        pass

    def callRegister(self):
        self.registerForm.show()
        pass

    def callWorkingWin(self):
        self.workingWindow.show()
        pass

    def cleanPwd(self):
        self.pwdCleaner.show()
        pass

    def msgBox(self, title, text):
        message = MessageBox(self, title, text)
        message.exec()

    def closeEvent(self, event):
        message = QuestionBox(self, '提示', "确定退出？")
        message.exec()
        if message.clickedBtn() == message.confirm_btn:
            event.accept()
            qApp.quit()
        else:
            event.ignore()


class RegisterForm(QWidget, Ui_RegisterForm):
    def __init__(self, parent=None):
        super(RegisterForm, self).__init__(parent)

        self.setupUi(self)
        self.setWindowIcon(QIcon(PICSRC + "icon.png"))
        self.setSlot()

    def setSlot(self):
        self.usr_let.editingFinished.connect(self.checker)
        self.pwd_let_1.editingFinished.connect(self.checker)
        self.pwd_let_2.editingFinished.connect(self.checker)
        self.ans_let.editingFinished.connect(self.checker)

        self.usr_let.textEdited.connect(self.cleanUsrHint)
        self.pwd_let_1.textEdited.connect(self.cleanPwd1Hint)
        self.pwd_let_2.textEdited.connect(self.cleanPwd2Hint)
        self.ans_let.textEdited.connect(self.cleanAnsHint)

        self.finish_btn.clicked.connect(self.tryRegister)
        pass

    def tryRegister(self):
        username = self.usr_let.text()
        password1 = self.pwd_let_1.text()
        password2 = self.pwd_let_2.text()
        question = self.question_cbx.currentText()
        answer = self.ans_let.text()

        if username == "" or password1 == "" or password2 == "" or \
                question == "" or answer == "":
            return False

        if not self.checker():
            return False

        f = open(UID, 'r+', encoding='utf-8')
        uid = f.readline()
        log = open(USERLOG, 'a+', encoding='utf-8')
        log.write(f"{username} {password1} {uid}")

        createDir(USERINF + str(int(uid)))

        with open(USERINF + str(int(uid)) + "/data.txt", 'w', encoding='utf-8') as data:
            initList = ["choice-question 0 0\n",
                        "true/false-question 0 0\n",
                        "fill-in-blank-question 0 0\n",
                        "short-answer-question 0 0\n"]
            data.writelines(initList)
        writeSingleLine(USERINF + str(int(uid)) + "/allPrevious.txt", "0 0\n")
        with open(USERINF + str(int(uid)) + "/safety.txt", 'w', encoding='utf-8') as safety:
            safety.write(' '.join([question, answer]) + '\n')

        uid = str(int(uid) + 1)
        f.seek(0)
        f.write(uid)

        self.msgBox("提示", "注册成功！请牢记您的用户名和密码！")
        self.close()
        pass

    def checker(self):
        username = self.usr_let.text()
        password1 = self.pwd_let_1.text()
        password2 = self.pwd_let_2.text()
        answer = self.ans_let.text()

        if not self.singleCheck(username, self.usr_hint, "用户名", checkUA):
            return False
        if hasUser(username):
            self.errorHint(self.usr_hint, "警告：用户名已存在")
            return False

        if not self.singleCheck(password1, self.pwd_hint_1, "密码", checkPwd):
            return False

        if password1 != password2:
            self.errorHint(self.pwd_hint_2, "警告：两次输入的密码不一致")
            return False

        if not self.singleCheck(answer, self.ans_hint, "问题答案", checkUA):
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

    def cleanUsrHint(self):
        self.usr_hint.clear()

    def cleanPwd1Hint(self):
        self.pwd_hint_1.clear()

    def cleanPwd2Hint(self):
        self.pwd_hint_2.clear()

    def cleanAnsHint(self):
        self.ans_hint.clear()

    def closeEvent(self, event):
        self.usr_let.clear()
        self.pwd_let_1.clear()
        self.pwd_let_2.clear()
        self.ans_let.clear()

        self.usr_hint.clear()
        self.pwd_hint_1.clear()
        self.pwd_hint_2.clear()
        self.ans_hint.clear()

        event.accept()

    def msgBox(self, title, text):
        message = MessageBox(self, title, text)
        message.exec()


class CleanPwd(QWidget, Ui_CleanPwd):
    def __init__(self, matrix, parent=None):
        super(CleanPwd, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix
        self.username = None
        self.uid = None
        self.ans = None

    def setSlot(self):
        self.usr_let.editingFinished.connect(self.checkUser)
        self.usr_let.textEdited.connect(self.cleanUsrHint)
        self.confirm_btn.clicked.connect(self.confirmQuestionAns)
        pass

    def checkUser(self):
        username = self.usr_let.text()
        if username == "":
            return False
        if hasUser(username):
            self.setUsrInf(username)
            return True
        else:
            self.errorHint(self.usr_hint, "警告：用户名不存在")
            return False
        pass

    def cleanUsrHint(self):
        self.usr_hint.clear()

    def confirmQuestionAns(self):
        if not self.checkUser():
            return False

        ans = self.questionAns_let.text()
        if ans == "":
            return False

        if ans != self.ans:
            self.msgBox("警告", "密保问题答案错误！请再次尝试！")
        else:
            with open(USERLOG, 'r', encoding='utf-8') as log:
                users = log.readlines()
                for i in range(len(users)):
                    if self.username in users[i].split():
                        users[i] = ' '.join([self.username, "114514", self.uid]) + '\n'
                        break

            with open(USERLOG, 'w', encoding='utf-8') as log:
                log.writelines(users)
            self.msgBox("提示", "您的密码已重置为114514！\n\n请登陆后立即修改密码！")
            self.close()
        pass

    def setUsrInf(self, username):
        self.username = username

        usrinf = getUser(username)
        self.usr_let.setText(str(username))
        usr, pwd, uid = usrinf.split()

        self.uid = uid
        with open(USERINF + str(int(uid)) + "/safety.txt", encoding='utf-8') as safety:
            question, ans = safety.readline().split()
        self.question_let.setText(str(question))
        self.ans = ans

    def msgBox(self, title, text):
        message = MessageBox(self, title, text)
        message.exec()

    @staticmethod
    def errorHint(hint, text):
        hint.setText(text)
        hint.setStyleSheet("color:red;")
        hint.show()

    def showEvent(self, event):
        self.matrix.setDisabled(True)
        event.accept()

    def closeEvent(self, event):
        self.matrix.setEnabled(True)
        self.usr_let.clear()
        self.question_let.clear()
        self.questionAns_let.clear()

        event.accept()
