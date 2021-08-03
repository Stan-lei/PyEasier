from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, qApp
from callUI.UIWIN.WorkingWindow import Ui_WorkingWindow
from callUI.call_Box import MessageBox
from callUI.call_Questions import *
from callUI.call_ChartDisplayer import ChartDisplayer
from callUI.call_UserCenter import UserCenter

from accessDatabase import *
from userCon.drawInf import *


class WorkingWindow(QMainWindow, Ui_WorkingWindow):
    def __init__(self, matrix, parent=None):
        super(WorkingWindow, self).__init__(parent)
        self.setupUi(self)
        self.welcome_pic.setPixmap(QPixmap(PICSRC + "welcome.jpg"))
        self.welcome_pic.setScaledContents(True)
        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix

        self.choiceQ = ChoiceQ(self)
        self.judgementQ = JudgementQ(self)
        self.fillinBlankQ = FillinBlankQ(self)
        self.shortAnsQ = ShortAnsQ(self)

        self.chartDisplayer = None
        self.userCenter = UserCenter(self)

        self.workingList = []

        self.setSlot()

    def setSlot(self):
        self.actionExit.triggered.connect(self.quitLogin)
        self.actionAnsSta.triggered.connect(self.displayChart)
        self.actionUserInf.triggered.connect(self.call_UserCenter)
        self.begin_btn.clicked.connect(self.beginTest)
        pass

    def displayChart(self):
        drawCharts()
        if self.chartDisplayer is None:
            self.chartDisplayer = ChartDisplayer(self)
        self.chartDisplayer.show()
        pass

    def call_UserCenter(self):
        self.userCenter.show()
        pass

    def cleanWrongQ(self):
        for item in self.workingList:
            item.cleanWrongQ()
        pass

    def beginTest(self):
        # TODO
        if not self.choiceQ_cbx.isChecked() and \
                not self.judgementQ_cbx.isChecked() and \
                not self.fillinBlankQ_cbx.isChecked() and \
                not self.shortAnsQ_cbx.isChecked():
            return False

        self.workingList.clear()
        if self.wrongSet_cbx.isChecked():
            self.wrongSetTest()
        else:
            self.normalTest()
        pass

    def normalTest(self):
        working = None
        qusetionNum = int(self.questionNum_sbx.text())
        if self.shortAnsQ_cbx.isChecked():
            self.shortAnsQ.initQuestions(randomSAQ(qusetionNum))
            working = self.setWorking(self.shortAnsQ, working)
            self.workingList.append(self.shortAnsQ)
        if self.fillinBlankQ_cbx.isChecked():
            self.fillinBlankQ.initQuestions(randomFBQ(qusetionNum))
            working = self.setWorking(self.fillinBlankQ, working)
            self.workingList.append(self.fillinBlankQ)
        if self.judgementQ_cbx.isChecked():
            self.judgementQ.initQuestions(randomJQ(qusetionNum))
            working = self.setWorking(self.judgementQ, working)
            self.workingList.append(self.judgementQ)
        if self.choiceQ_cbx.isChecked():
            self.choiceQ.initQuestions(randomCQ(qusetionNum))
            working = self.setWorking(self.choiceQ, working)
            self.workingList.append(self.choiceQ)
        self.hide()
        working.show()

    def wrongSetTest(self):  # TODO:
        working = None
        qusetionNum = int(self.questionNum_sbx.text())
        if self.shortAnsQ_cbx.isChecked():
            q_list = randomWSAQ(qusetionNum)
            if len(q_list) != 0:
                self.shortAnsQ.initQuestions(q_list=q_list)
                working = self.setWorking(self.shortAnsQ, working)
                self.workingList.append(self.shortAnsQ)
        if self.fillinBlankQ_cbx.isChecked():
            q_list = randomWFBQ(qusetionNum)
            if len(q_list) != 0:
                self.fillinBlankQ.initQuestions(q_list=q_list)
                working = self.setWorking(self.fillinBlankQ, working)
                self.workingList.append(self.fillinBlankQ)
        if self.judgementQ_cbx.isChecked():
            q_list = randomWJQ(qusetionNum)
            if len(q_list) != 0:
                self.judgementQ.initQuestions(q_list=q_list)
                working = self.setWorking(self.judgementQ, working)
                self.workingList.append(self.judgementQ)
        if self.choiceQ_cbx.isChecked():
            q_list = randomWCQ(qusetionNum)
            if len(q_list) != 0:
                self.choiceQ.initQuestions(q_list=q_list)
                working = self.setWorking(self.choiceQ, working)
                self.workingList.append(self.choiceQ)
        if working is not None:
            self.hide()
            working.show()
        else:
            self.msgBox("提示", "您还没有错题，请训练后再次查看！")
        pass

    @staticmethod
    def setWorking(q, working):
        if working is not None:
            working.before = q
        q.setBA(before=None, after=working)
        return q

    def finishTest(self):
        message = ["本次作答已完成"]
        DATA = self.getWorkingUserPath() + 'data.txt'
        ALLPRE = self.getWorkingUserPath() + 'allPrevious.txt'
        with open(DATA, 'r', encoding='utf-8') as data:
            lines = data.readlines()

        preCnt = 0
        preTotal = 0
        for working in self.workingList:
            message.insert(1, working.message + str(100 * working.rightCnt / len(working.q_list)) + '%')

            preCnt += working.rightCnt
            preTotal += len(working.q_list)

            for i in range(len(lines)):
                if working.type in lines[i]:
                    Qtype, right, total = lines[i].split()
                    right = str(int(right) + working.rightCnt)
                    total = str(int(total) + len(working.q_list))
                    lines[i] = ' '.join([Qtype, right, total]) + '\n'
                    break
        with open(DATA, 'w', encoding='utf-8') as data:
            data.writelines(lines)

        with open(ALLPRE, 'r+', encoding='utf-8') as allPrevious:
            lines = allPrevious.readlines()
            cnt, rate = lines[-1].split()
            allPrevious.write(' '.join([str(int(cnt) + 1), str(preCnt / preTotal)]) + '\n')

        message.append("请再接再厉！")

        self.msgBox("提示", "，\n".join(message))
        for working in self.workingList:
            working.hide()
            working.cleanBtn()
            working.cleanWrongQ()
        self.show()
        pass

    @staticmethod
    def getWorkingUserPath():
        f = open(WORKINGUSR, 'r', encoding='utf-8')
        usrname, pwd, uid = f.readline().split()
        PATH = USERINF + uid + '/'
        f.close()
        return PATH

    def msgBox(self, title, text):
        message = MessageBox(self, title, text)
        message.exec()

    def quitLogin(self):
        self.hide()
        self.matrix.show()
        pass

    def showEvent(self, event):
        self.matrix.usr_let.clear()
        self.matrix.pwd_let.clear()
        self.matrix.hide()
        event.accept()

    def closeEvent(self, event):
        message = QuestionBox(self, '提示', "确定退出？")
        message.exec()
        if message.clickedBtn() == message.confirm_btn:
            event.accept()
            qApp.quit()
        else:
            event.ignore()
