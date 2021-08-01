from pathlib import Path

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget
from callUI.UIWIN.ChartDisplayer import Ui_ChartDisplayer
from path import *


class ChartDisplayer(QWidget, Ui_ChartDisplayer):
    def __init__(self, matrix, parent=None):
        super(ChartDisplayer, self).__init__(parent)
        self.setupUi(self)
        self.setSlot()

        self.setWindowIcon(QIcon(PICSRC + "icon.png"))

        self.matrix = matrix
        self.displayBarChart()

    def setSlot(self):
        self.barChart_btn.clicked.connect(self.displayBarChart)
        self.pieChart_btn.clicked.connect(self.displayPieChart)
        self.lineChart_btn.clicked.connect(self.displayLineChart)
        pass

    def displayBarChart(self):
        self.displayChart("barChart.jpg")
        pass

    def displayPieChart(self):
        self.displayChart("pieChart.jpg")
        pass

    def displayLineChart(self):
        barPath = self.getWorkingUserPath() + "barChart.jpg"
        barPic = Path(barPath)
        if not barPic.exists():
            self.displayChart("lineChart.jpg")
        else:
            linePath = self.getWorkingUserPath() + "lineChart.jpg"
            linePic = Path(linePath)
            if not linePic.exists():
                self.pic_label.setText("您的做题次数过少，请至少训练4次后再来查看~")
            else:
                self.displayChart("lineChart.jpg")
        pass

    def displayChart(self, chart):
        chartPath = self.getWorkingUserPath() + chart
        pic = Path(chartPath)
        if pic.exists():
            self.pic_label.setPixmap(QPixmap(chartPath))
        else:
            self.pic_label.setPixmap(QPixmap(PICSRC + "404.jpg"))
        self.pic_label.setScaledContents(True)
        pass

    @staticmethod
    def getWorkingUserPath():
        with open(WORKINGUSR, 'r') as f:
            usrname, pwd, uid = f.readline().split()
            USERPATH = USERINF + uid + '/'
        return USERPATH

    def showEvent(self, event):
        self.setEnabled(True)
        self.matrix.setDisabled(True)
        self.displayBarChart()
        event.accept()

    def closeEvent(self, event):
        self.matrix.setEnabled(True)
        event.accept()

