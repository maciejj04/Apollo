# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
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
        MainWindow.resize(952, 639)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_3 = QtGui.QWidget(self.widget)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graphicsView = QtGui.QGraphicsView(self.widget_3)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout_2.addWidget(self.graphicsView)
        self.graphicsView_2 = QtGui.QGraphicsView(self.widget_3)
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.verticalLayout_2.addWidget(self.graphicsView_2)
        self.graphicsView_3 = QtGui.QGraphicsView(self.widget_3)
        self.graphicsView_3.setObjectName(_fromUtf8("graphicsView_3"))
        self.verticalLayout_2.addWidget(self.graphicsView_3)
        self.graphicsView.raise_()
        self.graphicsView_2.raise_()
        self.graphicsView_3.raise_()
        self.horizontalLayout.addWidget(self.widget_3)
        self.widget_4 = QtGui.QWidget(self.widget)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.formLayout = QtGui.QFormLayout(self.widget_4)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lcdNumber = QtGui.QLCDNumber(self.widget_4)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lcdNumber)
        self.lcdNumber.raise_()
        self.widget_3.raise_()
        self.horizontalLayout.addWidget(self.widget_4)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton = QtGui.QPushButton(self.widget_2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 952, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))

