# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_v2.ui'
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
        MainWindow.resize(1090, 884)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Apollo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pcmLcd = QtGui.QLCDNumber(self.centralwidget)
        self.pcmLcd.setGeometry(QtCore.QRect(990, 10, 91, 61))
        self.pcmLcd.setObjectName(_fromUtf8("pcmLcd"))
        self.FFTLcd = QtGui.QLCDNumber(self.centralwidget)
        self.FFTLcd.setGeometry(QtCore.QRect(990, 212, 91, 61))
        self.FFTLcd.setSmallDecimalPoint(False)
        self.FFTLcd.setObjectName(_fromUtf8("FFTLcd"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 822, 931, 41))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.loopbackCheckBox = QtGui.QCheckBox(self.layoutWidget)
        self.loopbackCheckBox.setObjectName(_fromUtf8("loopbackCheckBox"))
        self.horizontalLayout.addWidget(self.loopbackCheckBox)
        self.listen = QtGui.QCheckBox(self.layoutWidget)
        self.listen.setObjectName(_fromUtf8("listen"))
        self.horizontalLayout.addWidget(self.listen)
        self.startButton = QtGui.QPushButton(self.layoutWidget)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.recordButton = QtGui.QPushButton(self.layoutWidget)
        self.recordButton.setObjectName(_fromUtf8("recordButton"))
        self.horizontalLayout.addWidget(self.recordButton)
        self.personalFFTChart = PlotWidget(self.centralwidget)
        self.personalFFTChart.setGeometry(QtCore.QRect(12, 410, 931, 192))
        self.personalFFTChart.setObjectName(_fromUtf8("personalFFTChart"))
        self.personalPCMChart = PlotWidget(self.centralwidget)
        self.personalPCMChart.setGeometry(QtCore.QRect(12, 609, 931, 192))
        self.personalPCMChart.setObjectName(_fromUtf8("personalPCMChart"))
        self.fftsChart = PlotWidget(self.centralwidget)
        self.fftsChart.setGeometry(QtCore.QRect(12, 211, 931, 192))
        self.fftsChart.setObjectName(_fromUtf8("fftsChart"))
        self.pcmsChart = PlotWidget(self.centralwidget)
        self.pcmsChart.setGeometry(QtCore.QRect(12, 12, 931, 192))
        self.pcmsChart.setObjectName(_fromUtf8("pcmsChart"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 26))
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
        self.loopbackCheckBox.setText(_translate("MainWindow", "loopback", None))
        self.listen.setText(_translate("MainWindow", "listen", None))
        self.startButton.setText(_translate("MainWindow", "Start", None))
        self.recordButton.setText(_translate("MainWindow", "Record", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.actionChoose_file.setText(_translate("MainWindow", "Choose file ...", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
        self.actionChange_microphone.setText(_translate("MainWindow", "Change microphone", None))

from pyqtgraph import PlotWidget
