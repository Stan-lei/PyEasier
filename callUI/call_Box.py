from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from callUI.UIWIN.MessageBox import Ui_MessageBox
from callUI.UIWIN.Questionbox import Ui_QuestionBox
from path import PICSRC


class MessageBox(QDialog, Ui_MessageBox):
    def __init__(self, matrix, title, text, parent=None):
        super(MessageBox, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix
        self.setWindowTitle(title)
        self.text_lbl.setText(text)
        self.show()

    def setSlot(self):
        self.confirm_btn.clicked.connect(self.close)

    def showEvent(self, event):
        self.matrix.setDisabled(True)

    def closeEvent(self, event):
        self.matrix.setEnabled(True)


class QuestionBox(QDialog, Ui_QuestionBox):
    def __init__(self, matrix, title, text, parent=None):
        super(QuestionBox, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix
        self.setWindowTitle(title)
        self.text_lbl.setText(text)
        self._clicked_btn = self.cancel_btn
        self.show()

    def setSlot(self):
        self.confirm_btn.clicked.connect(self.confirm)
        self.cancel_btn.clicked.connect(self.cancel)

    def clickedBtn(self):
        return self._clicked_btn

    def confirm(self):
        self._clicked_btn = self.confirm_btn
        self.close()

    def cancel(self):
        self._clicked_btn = self.cancel_btn
        self.close()

    def showEvent(self, event):
        self.matrix.setDisabled(True)

    def closeEvent(self, event):
        self.matrix.setEnabled(True)
