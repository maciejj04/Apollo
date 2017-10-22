import numpy as np
import pyqtgraph
from PyQt4 import QtGui, QtCore

from src.Engine.Ear import Ear
from src.UI import ui_main
from src.UI import MainWindow
from src.Commons.Audio import Audio
from src.UI.drawOnce import drawOnce
from src.tools.helper_functions import getAudioFile
#from src.UIApi.API import showChooseMicrophoneDialog
from src.UI.ChooseMicrophoneView import ChooseMicrophoneView

class App(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.personalFFTChart.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 0
        self.startButton.clicked.connect(self.startButtonAction)
        self.listen.stateChanged.connect(self.update)
        self.actionChoose_file.triggered.connect(self.generateChooseFileDialog)
        self.actionChange_microphone.triggered.connect(self.showChooseMicrophoneDialog)
        self.recordButton.clicked.connect(self.recordButtonAction)
        self.ear = Ear()
        self.ear.stream_start()  # TODO: Do I need this here?
        
        self.fileFFTChart.plotItem.showGrid(True, True, 0.7)
    
    def update(self):
        
        if not self.listen.isChecked():
            return
        
        if self.ear.chunkData is not None and self.ear.fft is not None:
            pcmMax = np.max(np.abs(self.ear.chunkData))
            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.personalPCMChart.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(self.ear.fft) > self.maxFFT:
                self.maxFFT = np.max(np.abs(self.ear.fft))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.personalFFTChart.plotItem.setRange(yRange=[0, 1])
            
            pen = pyqtgraph.mkPen(color='b')
            self.personalPCMChart.plot(self.ear.datax, self.ear.chunkData, pen=pen, clear=True)
            
            pen = pyqtgraph.mkPen(color='r')
            self.personalFFTChart.plot(self.ear.fftx, self.ear.fft / self.maxFFT, pen=pen, clear=True)
        
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
    
    def generateChooseFileDialog(self):
        filePath = QtGui.QFileDialog.getOpenFileName()
        drawOnce(getAudioFile(filePath), self.fileFFTChart)

    def startButtonAction(self):
        print('dupa')

    def showChooseMicrophoneDialog(self):
        """
        :param mics: list of available microphones
        :return: choosen device nr.
        """
        ChooseMicrophoneView(parent=self)
   
    def recordButtonAction(self):
        # separate thread(?)
        self.ear.startRecording()