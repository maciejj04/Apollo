import pyaudio
from PyQt4 import QtGui
from src.UI.Ui_ChooseMicrophone import Ui_ChooseMicrophone
from src.Commons.InputDeviceInfo import InputDeviceInfo as Idi
from src.tools.Logger import Logger
from src.Engine.Ear import Ear

class ChooseMicrophoneView(QtGui.QMainWindow, Ui_ChooseMicrophone):
    
    chosenMic: int = None
    parent: Ear = None
    
    def __init__(self, parent=None):
        super(ChooseMicrophoneView, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.comboBox.addItems(list(Idi.foundDevices.values()))
        self.pushButton.clicked.connect(self.okAction)
        self.show()

    def okAction(self):
        index = self.comboBox.currentIndex()

        Idi.currentlyUsedDeviceIndex = index
        Logger.info("Changed microphone device to: " + str(index))
        self.parent.ear.close()
        self.parent.ear.pyAudio = pyaudio.PyAudio()
        self.parent.ear.stream_start()
        self.close()