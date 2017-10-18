# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 509, 781, 61))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.listen = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.listen.setObjectName(_fromUtf8("listen"))
        self.horizontalLayout.addWidget(self.listen)
        self.startButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.recordButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.recordButton.setObjectName(_fromUtf8("recordButton"))
        self.horizontalLayout.addWidget(self.recordButton)
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 781, 491))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.filePCMChart = PlotWidget(self.verticalLayoutWidget)
        self.filePCMChart.setObjectName(_fromUtf8("filePCMChart"))
        self.verticalLayout.addWidget(self.filePCMChart)
        self.fileFFTChart = PlotWidget(self.verticalLayoutWidget)
        self.fileFFTChart.setObjectName(_fromUtf8("fileFFTChart"))
        self.verticalLayout.addWidget(self.fileFFTChart)
        self.personalFFTChart = PlotWidget(self.verticalLayoutWidget)
        self.personalFFTChart.setObjectName(_fromUtf8("personalFFTChart"))
        self.verticalLayout.addWidget(self.personalFFTChart)
        self.personalPCMChart = PlotWidget(self.verticalLayoutWidget)
        self.personalPCMChart.setObjectName(_fromUtf8("personalPCMChart"))
        self.verticalLayout.addWidget(self.personalPCMChart)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menubar)
        self.actionChoose_file = QtGui.QAction(MainWindow)
        self.actionChoose_file.setObjectName(_fromUtf8("actionChoose_file"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionChange_microphone = QtGui.QAction(MainWindow)
        self.actionChange_microphone.setObjectName(_fromUtf8("actionChange_microphone"))
        self.menuOptions.addAction(self.actionChoose_file)
        self.menuOptions.addAction(self.actionSettings)
        self.menuOptions.addAction(self.actionChange_microphone)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Apollo", None))
        self.listen.setText(_translate("MainWindow", "listen", None))
        self.startButton.setText(_translate("MainWindow", "Start", None))
        self.recordButton.setText(_translate("MainWindow", "Record", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.actionChoose_file.setText(_translate("MainWindow", "Choose file ...", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
        self.actionChange_microphone.setText(_translate("MainWindow", "Change microphone", None))

from pyqtgraph import PlotWidget
