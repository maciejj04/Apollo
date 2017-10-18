# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(772, 631)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listen = QtGui.QCheckBox(self.centralwidget)
        self.listen.setObjectName(_fromUtf8("listen"))
        self.verticalLayout.addWidget(self.listen)
        self.filePCMChart = PlotWidget(self.centralwidget)
        self.filePCMChart.setObjectName(_fromUtf8("filePCMChart"))
        self.verticalLayout.addWidget(self.filePCMChart)
        self.fileFFTChart = PlotWidget(self.centralwidget)
        self.fileFFTChart.setObjectName(_fromUtf8("fileFFTChart"))
        self.verticalLayout.addWidget(self.fileFFTChart)
        self.personalFFTChart = PlotWidget(self.centralwidget)
        self.personalFFTChart.setObjectName(_fromUtf8("personalFFTChart"))
        self.verticalLayout.addWidget(self.personalFFTChart)
        self.personalPCMChart = PlotWidget(self.centralwidget)
        self.personalPCMChart.setObjectName(_fromUtf8("personalPCMChart"))
        self.verticalLayout.addWidget(self.personalPCMChart)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 772, 26))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuOptions = QtGui.QMenu(self.menuBar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionChoose_file = QtGui.QAction(MainWindow)
        self.actionChoose_file.setObjectName(_fromUtf8("actionChoose_file"))
        self.menuOptions.addAction(self.actionChoose_file)
        self.menuBar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.listen.setText(_translate("MainWindow", "listen", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.actionChoose_file.setText(_translate("MainWindow", "Choose file ...", None))

from pyqtgraph import PlotWidget
