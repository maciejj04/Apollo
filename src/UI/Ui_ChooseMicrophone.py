# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ChooseMicrophone.ui'
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

class Ui_ChooseMicrophone(object):
    def setupUi(self, ChooseMicrophone):
        ChooseMicrophone.setObjectName(_fromUtf8("ChooseMicrophone"))
        ChooseMicrophone.resize(511, 88)
        self.centralwidget = QtGui.QWidget(ChooseMicrophone)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 491, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 50, 141, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        ChooseMicrophone.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChooseMicrophone)
        QtCore.QMetaObject.connectSlotsByName(ChooseMicrophone)

    def retranslateUi(self, ChooseMicrophone):
        ChooseMicrophone.setWindowTitle(_translate("ChooseMicrophone", "MainWindow", None))
        self.pushButton.setText(_translate("ChooseMicrophone", "Ok", None))

