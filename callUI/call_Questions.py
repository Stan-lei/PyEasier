import abc

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from callUI.UIWIN.ChoiceQ import Ui_ChoiceQ
from callUI.UIWIN.JudgementQ import Ui_JudgementQ
from callUI.UIWIN.ShortAnswerQ import Ui_ShortAnswerQ
from callUI.UIWIN.FillinBlankQ import Ui_FillinBlankQ
from callUI.call_Box import QuestionBox
import pandas as pd
from path import PICSRC, WCHOICEQ, WFILLINBLANKQ, WJUDGEMENTQ


class AbstractQuestion(object):
    @abc.abstractmethod
    def initQuestions(self, q_list):
        pass

    @abc.abstractmethod
    def setQuestion(self, index):
        pass

    @abc.abstractmethod
    def preQuestion(self):
        pass

    @abc.abstractmethod
    def nextQuestion(self):
        pass

    def setBA(self, before, after):
        pass


class ChoiceQ(QWidget, Ui_ChoiceQ, AbstractQuestion):
    def __init__(self, matrix, parent=None):
        super(ChoiceQ, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix  # return
        self.q_list = None
        self.rightCnt = 0
        self.message = "选择题的正确率为"
        self.type = "choice-question"

        self.wrongQ = []

        self.checked = []
        self.index = 0

        self.dic = {'A': self.A_btn, 'B': self.B_btn,
                    'C': self.C_btn, 'D': self.D_btn}

        self.before = None
        self.after = None

        self.setSlot()

    def setSlot(self):
        self.previous_btn.clicked.connect(self.preQuestion)
        self.next_btn.clicked.connect(self.nextQuestion)

        self.A_btn.clicked.connect(self.clickedA_btn)
        self.B_btn.clicked.connect(self.clickedB_btn)
        self.C_btn.clicked.connect(self.clickedC_btn)
        self.D_btn.clicked.connect(self.clickedD_btn)

        self.getAns_btn.clicked.connect(self.clickedGetAns_btn)

        pass

    def clickedA_btn(self):
        if self.A_btn.isChecked():
            self.checked[self.index][1].append('A')
        else:
            self.checked[self.index][1].remove('A')

    def clickedB_btn(self):
        if self.B_btn.isChecked():
            self.checked[self.index][1].append('B')
        else:
            self.checked[self.index][1].remove('B')

    def clickedC_btn(self):
        if self.C_btn.isChecked():
            self.checked[self.index][1].append('C')
        else:
            self.checked[self.index][1].remove('C')

    def clickedD_btn(self):
        if self.D_btn.isChecked():
            self.checked[self.index][1].append('D')
        else:
            self.checked[self.index][1].remove('D')

    def clickedGetAns_btn(self):
        if len(self.checked[self.index][1]) == 0:
            return False
        self.checkAns()

    def initQuestions(self, q_list):
        abstractInitQuestions(self, q_list)
        pass

    def checkAns(self):
        self.A_btn.setStyleSheet("")
        self.B_btn.setStyleSheet("")
        self.C_btn.setStyleSheet("")
        self.D_btn.setStyleSheet("")

        ans = getStr(self.q_list[self.index]['ans'])
        self.A_btn.setEnabled(False)
        self.B_btn.setEnabled(False)
        self.C_btn.setEnabled(False)
        self.D_btn.setEnabled(False)

        self.A_btn.setChecked(False)
        self.B_btn.setChecked(False)
        self.C_btn.setChecked(False)
        self.D_btn.setChecked(False)

        for x in ans:
            self.dic[x].setStyleSheet("background-color: rgb(112, 193, 179);")
        right = False
        for x in self.checked[self.index][1]:
            if x not in ans:
                self.dic[x].setStyleSheet("background-color: rgb(229, 92, 92);")
            else:
                right = True
        if not self.checked[self.index][0]:
            if right:
                self.rightCnt += 1
            else:
                self.wrongQ.append(self.q_list[self.index])

        self.checked[self.index][0] = True

    def cleanBtn(self):
        self.A_btn.setEnabled(True)
        self.B_btn.setEnabled(True)
        self.C_btn.setEnabled(True)
        self.D_btn.setEnabled(True)

        self.A_btn.setChecked(False)
        self.B_btn.setChecked(False)
        self.C_btn.setChecked(False)
        self.D_btn.setChecked(False)

        self.A_btn.setStyleSheet("")
        self.B_btn.setStyleSheet("")
        self.C_btn.setStyleSheet("")
        self.D_btn.setStyleSheet("")

    def setQuestion(self, index):
        self.index = index
        self.question_text.setText(getStr(self.q_list[index]['question']))
        self.A_textEdit.setText(getStr(self.q_list[index]['A']))
        self.B_textEdit.setText(getStr(self.q_list[index]['B']))
        self.C_textEdit.setText(getStr(self.q_list[index]['C']))
        self.D_textEdit.setText(getStr(self.q_list[index]['D']))

    def preQuestion(self):
        abstractPre(self)
        pass

    def nextQuestion(self):
        abstractNext(self)
        pass

    def setBA(self, before, after):
        self.before = before
        self.after = after

    def cleanWrongQ(self):
        df = pd.read_excel(WCHOICEQ)
        question = list(df['question'])
        A = list(df['A'])
        B = list(df['B'])
        C = list(df['C'])
        D = list(df['D'])
        ans = list(df['ans'])

        for item in self.wrongQ:
            str_q = getStr(item['question'])
            if str_q not in question:
                question.append(str_q)
                A.append(getStr(item['A']))
                B.append(getStr(item['B']))
                C.append(getStr(item['C']))
                D.append(getStr(item['D']))
                ans.append(getStr(item['ans']))
        data = {'question': question,
                'A': A, 'B': B, 'C': C, 'D': D,
                'ans': ans}
        self.wrongQ.clear()
        df = pd.DataFrame(data)
        df.to_excel(WCHOICEQ)
        pass

    def showEvent(self, event):
        workingList = self.matrix.workingList
        length = len(workingList)
        total = len(self.q_list)
        self.index_lbl.setText(f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
                               f"共{total * length}题")
        event.accept()

    def closeEvent(self, event):
        abstractCloseEvent(self, event)


class JudgementQ(QWidget, Ui_JudgementQ, AbstractQuestion):
    def __init__(self, matrix, parent=None):
        super(JudgementQ, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix  # return
        self.q_list = None
        self.rightCnt = 0
        self.message = "判断题的正确率为"
        self.type = "true/false-question"

        self.wrongQ = []

        self.checked = []
        self.index = 0

        self.dic = {'T': self.True_btn, 'F': self.False_btn}

        self.before = None
        self.after = None

        self.setSlot()

    def setSlot(self):
        self.previous_btn.clicked.connect(self.preQuestion)
        self.next_btn.clicked.connect(self.nextQuestion)

        self.True_btn.clicked.connect(self.clickedT_btn)
        self.False_btn.clicked.connect(self.clickedF_btn)
        pass

    def clickedT_btn(self):
        self.checked[self.index][1].append('T')
        self.checkAns()
        pass

    def clickedF_btn(self):
        self.checked[self.index][1].append('F')
        self.checkAns()
        pass

    def checkAns(self):
        self.True_btn.setStyleSheet("")
        self.False_btn.setStyleSheet("")

        ans = getStr(self.q_list[self.index]['ans'])
        self.True_btn.setEnabled(False)
        self.False_btn.setEnabled(False)

        for x in ans:
            self.dic[x].setStyleSheet("background-color: rgb(112, 193, 179);")
        right = False
        for x in self.checked[self.index][1]:
            if x not in ans:
                self.dic[x].setStyleSheet("background-color: rgb(229, 92, 92);")
            else:
                right = True

        if not self.checked[self.index][0]:
            if right:
                self.rightCnt += 1
            else:
                self.wrongQ.append(self.q_list[self.index])

        self.checked[self.index][0] = True
        pass

    def cleanBtn(self):
        self.True_btn.setEnabled(True)
        self.False_btn.setEnabled(True)
        self.True_btn.setStyleSheet("")
        self.False_btn.setStyleSheet("")

    def initQuestions(self, q_list):
        abstractInitQuestions(self, q_list)
        pass

    def setQuestion(self, index):
        self.index = index
        self.question_text.setText(getStr(self.q_list[index]['question']))
        pass

    def preQuestion(self):
        abstractPre(self)
        pass

    def nextQuestion(self):
        abstractNext(self)
        pass

    def setBA(self, before, after):
        self.before = before
        self.after = after

    def cleanWrongQ(self):
        df = pd.read_excel(WJUDGEMENTQ)
        question = list(df['question'])
        ans = list(df['ans'])

        for item in self.wrongQ:
            str_q = getStr(item['question'])
            if str_q not in question:
                question.append(str_q)
                ans.append(getStr(item['ans']))
        data = {'question': question,
                'ans': ans}
        self.wrongQ.clear()
        df = pd.DataFrame(data)
        df.to_excel(WJUDGEMENTQ)
        pass

    def showEvent(self, event):
        workingList = self.matrix.workingList
        length = len(workingList)
        total = len(self.q_list)
        self.index_lbl.setText(f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
                               f"共{total * length}题")
        event.accept()

    def closeEvent(self, event):
        abstractCloseEvent(self, event)


class ShortAnsQ(QWidget, Ui_ShortAnswerQ, AbstractQuestion):
    def __init__(self, matrix, parent=None):
        super(ShortAnsQ, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix  # return
        self.q_list = None
        self.rightCnt = 0
        self.message = "简答题的正确率为"
        self.type = "short-answer-question"

        self.wrongQ = []

        self.checked = []
        self.index = 0

        self.before = None
        self.after = None

        self.setSlot()

    def setSlot(self):
        self.previous_btn.clicked.connect(self.preQuestion)
        self.next_btn.clicked.connect(self.nextQuestion)

        self.answer_btn.clicked.connect(self.clickStop_btn)
        pass

    def clickStop_btn(self):
        ansAreaText = self.ansArea_text.toPlainText()
        if ansAreaText == "":
            return False
        self.checked[self.index][1].append(ansAreaText)
        self.checkAns()
        pass

    def checkAns(self):
        self.answer_btn.setEnabled(False)
        self.answer_text.setText(getStr(self.q_list[self.index]['ans']))
        self.ansArea_text.setText('\n'.join(self.checked[self.index][1]))

        if not self.checked[self.index][0]:
            self.rightCnt += 1
        self.checked[self.index][0] = True
        pass

    def cleanBtn(self):
        self.answer_btn.setEnabled(True)
        self.ansArea_text.setText("")
        self.answer_text.setText("")

    def initQuestions(self, q_list):
        abstractInitQuestions(self, q_list)
        pass

    def setQuestion(self, index):
        self.index = index
        self.question_text.setText(getStr(self.q_list[index]['question']))
        pass

    def preQuestion(self):
        abstractPre(self)
        pass

    def nextQuestion(self):
        abstractNext(self)
        pass

    def setBA(self, before, after):
        self.before = before
        self.after = after

    def cleanWrongQ(self):
        # assert all shortAns questions han no wrong ans
        pass

    def showEvent(self, event):
        workingList = self.matrix.workingList
        length = len(workingList)
        total = len(self.q_list)
        self.index_lbl.setText(
            f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
            f"共{total * length}题")
        event.accept()

    def closeEvent(self, event):
        abstractCloseEvent(self, event)


class FillinBlankQ(QWidget, Ui_FillinBlankQ, AbstractQuestion):
    def __init__(self, matrix, parent=None):
        super(FillinBlankQ, self).__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix  # return
        self.q_list = None
        self.rightCnt = 0
        self.message = "填空题的正确率为"
        self.type = "fill-in-blank-question"

        self.wrongQ = []

        self.checked = []
        self.index = 0

        self.before = None
        self.after = None

        self.setSlot()

    def setSlot(self):
        self.previous_btn.clicked.connect(self.preQuestion)
        self.next_btn.clicked.connect(self.nextQuestion)

        self.answer_btn.clicked.connect(self.clickStop_btn)
        pass

    def clickStop_btn(self):
        ansAreaText = self.ansArea_text.text()
        if ansAreaText == "":
            return False
        self.checked[self.index][1].append(ansAreaText)
        self.checkAns()
        pass

    def checkAns(self):
        self.answer_btn.setStyleSheet("")

        ans = getStr(self.q_list[self.index]['ans'])
        self.answer_btn.setEnabled(False)

        self.answer_text.setText(ans)
        self.ansArea_text.setText(''.join(self.checked[self.index][1]))

        right = False
        if ''.join(self.checked[self.index][1]) == ans:
            self.answer_btn.setStyleSheet("background-color: rgb(112, 193, 179);")  # right color
            right = True
        else:
            self.answer_btn.setStyleSheet("background-color: rgb(229, 92, 92);")  # wrong color

        if not self.checked[self.index][0]:
            if right:
                self.rightCnt += 1
            else:
                self.wrongQ.append(self.q_list[self.index])

        self.checked[self.index][0] = True
        pass

    def cleanBtn(self):
        self.answer_btn.setEnabled(True)
        self.ansArea_text.setText("")
        self.answer_text.setText("")
        self.answer_btn.setStyleSheet("")

    def initQuestions(self, q_list):
        abstractInitQuestions(self, q_list)
        pass

    def setQuestion(self, index):
        self.index = index
        self.question_text.setText(getStr(self.q_list[index]['question']))
        pass

    def preQuestion(self):
        abstractPre(self)
        pass

    def nextQuestion(self):
        abstractNext(self)
        pass

    def setBA(self, before, after):
        self.before = before
        self.after = after

    def cleanWrongQ(self):
        df = pd.read_excel(WFILLINBLANKQ)
        question = list(df['question'])
        ans = list(df['ans'])

        for item in self.wrongQ:
            str_q = getStr(item['question'])
            if str_q not in question:
                question.append(str_q)
                ans.append(getStr(item['ans']))
        data = {'question': question,
                'ans': ans}
        self.wrongQ.clear()
        df = pd.DataFrame(data)
        df.to_excel(WFILLINBLANKQ)
        pass

    def showEvent(self, event):
        workingList = self.matrix.workingList
        length = len(workingList)
        total = len(self.q_list)
        self.index_lbl.setText(f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
                               f"共{total * length}题")
        event.accept()

    def closeEvent(self, event):
        abstractCloseEvent(self, event)


def getStr(value):
    n = 0
    s = ""
    for x in value.array:
        if n > 0:
            s += '\n'
        s += str(x)
        n += 1
    return s


def switchQuestions(self, another):
    another.move(self.x(), self.y())
    another.show()
    self.hide()
    pass


def abstractInitQuestions(self, q_list):
    self.q_list = q_list
    self.rightCnt = 0
    self.checked.clear()
    for i in range(len(q_list)):
        self.checked.append([False, []])
    self.setQuestion(0)


def abstractPre(self):
    if self.index == 0:
        if self.before is None:
            return False
        else:
            switchQuestions(self, self.before)
            return True
    self.setQuestion(self.index - 1)

    con = self.checked[self.index][0]
    workingList = self.matrix.workingList
    length = len(workingList)
    total = len(self.q_list)
    self.index_lbl.setText(f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
                           f"共{total * length}题")

    if con:
        self.checkAns()
    else:
        self.cleanBtn()


def abstractNext(self):
    if self.index == len(self.q_list) - 1:
        if self.after is None:
            if checkedUnfinished(self):
                return False
            self.matrix.finishTest()
            return True
        else:
            switchQuestions(self, self.after)
            return True
    self.setQuestion(self.index + 1)

    con = self.checked[self.index][0]
    workingList = self.matrix.workingList
    length = len(workingList)
    total = len(self.q_list)
    self.index_lbl.setText(f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
                           f"共{total * length}题")

    if con:
        self.checkAns()
    else:
        self.cleanBtn()


def abstractCloseEvent(self, event):
    message = QuestionBox(self, '提示', "作答尚未完成，\n本次答题数据将不会被记录，是否退出？")
    message.exec()
    if message.clickedBtn() == message.confirm_btn:
        event.accept()
        self.cleanBtn()
        self.matrix.show()
    else:
        event.ignore()


def checkedUnfinished(self):
    while self is not None:
        for i in range(len(self.q_list) - 1, -1, -1):
            if not self.checked[i][0]:
                self.close()
                self.setQuestion(i)
                workingList = self.matrix.workingList
                length = len(workingList)
                total = len(self.q_list)
                self.index_lbl.setText(f"第{total * (length - workingList.index(self) - 1) + self.index + 1}题/"
                                       f"共{total * length}题")
                self.cleanBtn()
                return True
        self = self.before
    return False
