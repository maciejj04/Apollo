import sys
from PyQt4 import QtGui
from src.UI.Ui_ChooseMicrophone import Ui_ChooseMicrophone
from src.Commons.InputDeviceInfo import InputDeviceInfo as Idi


class ChooseMicrophoneView(QtGui.QMainWindow, Ui_ChooseMicrophone):
    def __init__(self, micList, parent=None):
        super(ChooseMicrophoneView, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.addItems('DUPA')
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        self.pushButton.clicked.connect(self.close)
        # self.show()
    
    def selectionchange(self, i):
        print("You choose: %d" % i)
        
        # Idi.currentlyUsedDeviceIndex = dialog.
