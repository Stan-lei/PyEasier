# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ChartDisplayer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChartDisplayer(object):
    def setupUi(self, ChartDisplayer):
        ChartDisplayer.setObjectName("ChartDisplayer")
        ChartDisplayer.resize(800, 600)
        ChartDisplayer.setMinimumSize(QtCore.QSize(800, 600))
        ChartDisplayer.setMaximumSize(QtCore.QSize(800, 600))
        ChartDisplayer.setStyleSheet("background-color: rgb(255, 170, 173);")
        self.pic_label = QtWidgets.QLabel(ChartDisplayer)
        self.pic_label.setGeometry(QtCore.QRect(80, 20, 640, 480))
        self.pic_label.setMinimumSize(QtCore.QSize(640, 480))
        self.pic_label.setMaximumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setFamily("方正小标宋简体")
        font.setPointSize(12)
        self.pic_label.setFont(font)
        self.pic_label.setText("")
        self.pic_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pic_label.setObjectName("pic_label")
        self.barChart_btn = QtWidgets.QPushButton(ChartDisplayer)
        self.barChart_btn.setGeometry(QtCore.QRect(160, 520, 120, 40))
        font = QtGui.QFont()
        font.setFamily("方正小标宋简体")
        font.setPointSize(10)
        self.barChart_btn.setFont(font)
        self.barChart_btn.setObjectName("barChart_btn")
        self.pieChart_btn = QtWidgets.QPushButton(ChartDisplayer)
        self.pieChart_btn.setGeometry(QtCore.QRect(340, 520, 120, 40))
        font = QtGui.QFont()
        font.setFamily("方正小标宋简体")
        font.setPointSize(10)
        self.pieChart_btn.setFont(font)
        self.pieChart_btn.setObjectName("pieChart_btn")
        self.lineChart_btn = QtWidgets.QPushButton(ChartDisplayer)
        self.lineChart_btn.setGeometry(QtCore.QRect(520, 520, 120, 40))
        font = QtGui.QFont()
        font.setFamily("方正小标宋简体")
        font.setPointSize(10)
        self.lineChart_btn.setFont(font)
        self.lineChart_btn.setObjectName("lineChart_btn")

        self.retranslateUi(ChartDisplayer)
        QtCore.QMetaObject.connectSlotsByName(ChartDisplayer)

    def retranslateUi(self, ChartDisplayer):
        _translate = QtCore.QCoreApplication.translate
        ChartDisplayer.setWindowTitle(_translate("ChartDisplayer", "答题情况"))
        self.barChart_btn.setText(_translate("ChartDisplayer", "题型正确率"))
        self.pieChart_btn.setText(_translate("ChartDisplayer", "题量分布"))
        self.lineChart_btn.setText(_translate("ChartDisplayer", "正确率趋势"))
