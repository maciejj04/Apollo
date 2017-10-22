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
        MainWindow.resize(980, 749)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Apollo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
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
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.listen = QtGui.QCheckBox(self.centralwidget)
        self.listen.setObjectName(_fromUtf8("listen"))
        self.horizontalLayout.addWidget(self.listen)
        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.recordButton = QtGui.QPushButton(self.centralwidget)
        self.recordButton.setObjectName(_fromUtf8("recordButton"))
        self.horizontalLayout.addWidget(self.recordButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 980, 26))
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
