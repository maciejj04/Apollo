import numpy as np
import pyqtgraph
from PyQt4 import QtGui, QtCore

from src.Engine.Ear import Ear
from src.UI import MainWindow
from src.UI.ChooseMicrophoneView import ChooseMicrophoneView
from src.Engine.ProcessingEngine import ProcessingEngine
from src.Commons.Audio import Audio

class App(QtGui.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')
        super(App, self).__init__(parent)
        #pyqtgraph.setConfigOption(useOpenGL=True)
        self.setupUi(self)
        self.resize(1300, 900)
        self.personalFFTChart.plotItem.showGrid(True, True, 0.7)

# TODO: to be deleted. Just for evaluation.
        x = np.arange(1000)
        y = np.random.normal(size=(3, 1000))
        for i in range(3):
            self.filePCMChart.plot(x, y[i], pen=(i, 3))
        
        self.maxFFT = 0
        self.maxPCM = 0
        self.startButton.clicked.connect(self.startButtonAction)
        self.listen.stateChanged.connect(self.update)
        self.actionChoose_file.triggered.connect(self.generateChooseFileDialog)
        self.actionChange_microphone.triggered.connect(self.showChooseMicrophoneDialog)
        self.recordButton.clicked.connect(self.recordButtonAction)
        self.ear = Ear()
        self.processingEngine = ProcessingEngine()
        self.ear.addObserver(self.processingEngine)
        #TODO: move drawOce invocation underneath! Requires getting raw audio data!
        self.liveProcessingEngine = ProcessingEngine(Audio().loadFromPathAndAdjust().getRawDataFromWav())
        
        self._drawOnce(
            chart=self.fileFFTChart,
            yData=self.liveProcessingEngine.calculateFrequencyEnvelope(),
            #  (min, max) = self.liveProcessingEngine.calculateMinMaxFrequencies()
            yRange=[0, 2000]
        )
        
        
        self.ear.stream_start()  # TODO: Do I need this here?
        
        self.fileFFTChart.plotItem.showGrid(True, True, 0.7)
    
    def update(self):
        
        if not self.listen.isChecked():
            return
        
        chunksFFT = self.processingEngine.getCurrentRTChunkFFT()
        chunksData = self.processingEngine.getCurrentRTChunk().rawData
        
        if chunksData is not None and chunksFFT is not None:
            pcmMax = np.max(np.abs(chunksData))
            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.personalPCMChart.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(chunksFFT) > self.maxFFT:
                self.maxFFT = np.max(np.abs(chunksFFT))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.personalFFTChart.plotItem.setRange(yRange=[0, 1])
            
            pen = pyqtgraph.mkPen(color='b')
            self.personalPCMChart.plot(self.ear.datax, chunksData, pen=pen, clear=True)
            
            pen = pyqtgraph.mkPen(color='r')
            self.personalFFTChart.plot(self.processingEngine.getCurrentRTChunkFreq(), chunksFFT/self.maxFFT, pen=pen, clear=True)
        
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
    
    def generateChooseFileDialog(self):
        filePath = QtGui.QFileDialog.getOpenFileName()
        #TODO: !!!!!!!!!!!!!!!!!!!!!!!!!
        self._drawOnce(
            chart=self.fileFFTChart,
            yData=self.liveProcessingEngine.calculateFrequencyEnvelope(),
            #  (min, max) = self.liveProcessingEngine.calculateMinMaxFrequencies()
            yRange=[0, 2000]
        )

    def startButtonAction(self):
        print('Action')

    def showChooseMicrophoneDialog(self):
        """
        :param mics: list of available microphones
        :return: choosen device nr.
        """
        ChooseMicrophoneView(parent=self)
   
    def recordButtonAction(self):
        # separate thread(?)
        self.ear.startRecording()



    def _drawOnce(self, chart, yData, yRange=[0, 2000]):
        """
        :param chart: pyqtgraph object to draw on
        :return: void
        """
        # color = pyqtgraph.hsvColor(time.time() / 5 % 1, alpha=.5)
        pen = pyqtgraph.mkPen(color='r', width=2)
    
        # TODO: find coorelation between np.int16 and PyAudio data types. Do We need PyAudio?
    
    
        
        chart.setRange(yRange=yRange)
        chart.plot(y=yData, pen=pen, clear=True)

    def _getLastNSeconds(self, data):
        return