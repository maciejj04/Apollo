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
        MainWindow.resize(1116, 820)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Apollo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.personalFFTChart = PlotWidget(self.widget)
        self.personalFFTChart.setObjectName(_fromUtf8("personalFFTChart"))
        self.horizontalLayout_2.addWidget(self.personalFFTChart)
        self.verticalLayout_2.addWidget(self.widget)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.fftsChart = PlotWidget(self.frame)
        self.fftsChart.setObjectName(_fromUtf8("fftsChart"))
        self.horizontalLayout_4.addWidget(self.fftsChart)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.HzDiffLcd = QtGui.QLCDNumber(self.frame)
        self.HzDiffLcd.setObjectName(_fromUtf8("HzDiffLcd"))
        self.gridLayout.addWidget(self.HzDiffLcd, 1, 1, 1, 1)
        self.HzLcd = QtGui.QLCDNumber(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.HzLcd.setFont(font)
        self.HzLcd.setObjectName(_fromUtf8("HzLcd"))
        self.gridLayout.addWidget(self.HzLcd, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pcmsChart = PlotWidget(self.frame_2)
        self.pcmsChart.setObjectName(_fromUtf8("pcmsChart"))
        self.horizontalLayout_3.addWidget(self.pcmsChart)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.playbackCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.playbackCheckBox.setObjectName(_fromUtf8("playbackCheckBox"))
        self.horizontalLayout.addWidget(self.playbackCheckBox)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1116, 26))
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
        self.label.setText(_translate("MainWindow", "Hz", None))
        self.label_2.setText(_translate("MainWindow", "Hz Diff", None))
        self.playbackCheckBox.setText(_translate("MainWindow", "playback", None))
        self.listen.setText(_translate("MainWindow", "listen", None))
        self.startButton.setText(_translate("MainWindow", "Start", None))
        self.recordButton.setText(_translate("MainWindow", "Record", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.actionChoose_file.setText(_translate("MainWindow", "Choose file ...", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))
        self.actionChange_microphone.setText(_translate("MainWindow", "Change microphone", None))

from pyqtgraph import PlotWidget
