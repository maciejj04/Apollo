import numpy as np
import pyqtgraph
import pyaudio
from PyQt4 import QtGui, QtCore

from src.Engine.Ear import Ear
from src.UI import MainWindow
from src.UI import MainWindow_v2
from src.UI.ChooseMicrophoneView import ChooseMicrophoneView
from src.Engine.ProcessingEngine import ProcessingEngine
from src.Commons.Audio import Audio
from src.MessageServer import MessageServer, MsgTypes
from src.MessageClient import MessageClient
from src.StreamHandlers.OutputStreamHandler import OutputStreamHandler
from src.Engine.StaticAudio import StaticAudio

class App(QtGui.QMainWindow, MainWindow.Ui_MainWindow):#, MessageClient
    class _Chart:
        pass
    
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')
        super(App, self).__init__(parent)
        MessageServer.registerForEvent(self, MsgTypes.UPDATE_PCM_CHART)
        self.setupUi(self)
        self.resize(1300, 900)
        self.personalFFTChart.plotItem.showGrid(True, True, 0.7)
        self.fftsChart.plotItem.showGrid(True, True, 0.7)
        self.pcmsChart.plotItem.showGrid(True, True, 0.7)
        
        self.maxFFT = 0
        self.maxPCM = 0
        self.loopbackCheckBox.stateChanged.connect(self._loopbackCheckBoxAction)
        self.startButton.clicked.connect(self.startButtonAction)
        self.listen.stateChanged.connect(self.update)
        self.actionChoose_file.triggered.connect(self.generateChooseFileDialog)
        self.actionChange_microphone.triggered.connect(self.showChooseMicrophoneDialog)
        self.recordButton.clicked.connect(self.recordButtonAction)
        self.ear = Ear()
        rawInputAudioData = Audio().loadFromPathAndAdjust().getRawDataFromWav()
        self.liveProcessingEngine = ProcessingEngine()
        self.ear.addObserver(self.liveProcessingEngine)
        self.staticProcessingEngine = ProcessingEngine(rawInputAudioData)
        self.loopbackStreamHandler = OutputStreamHandler(StaticAudio(rawInputAudioData))

        
        # self._drawOnce(
        #     chart=self.fftsChart,
        #     yData=self.liveProcessingEngine.calculateFrequencyEnvelope(),
        #     #  (min, max) = self.liveProcessingEngine.calculateMinMaxFrequencies()
        #     yRange=[0, 2000]
        # )
        self.pcmsChart.plot(y=self.staticProcessingEngine.fullAudioData, pen='r')
        self._updateFftsChart()
        
        self.ear.stream_start()  # TODO: Do I need this here?
    
    def update(self):
        
        if not self.listen.isChecked():
            return
        
        chunksFFT = self.liveProcessingEngine.getCurrentRTChunkFFT()
        chunkData = self.liveProcessingEngine.getCurrentRTChunk().rawData
        
        if chunkData is not None and chunksFFT is not None:
            # pcmMax = np.max(np.abs(chunkData))
            # if pcmMax > self.maxPCM:
            #     self.maxPCM = pcmMax
            #     self.personalPCMChart.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(chunksFFT) > self.maxFFT:
                self.maxFFT = np.max(np.abs(chunksFFT))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.personalFFTChart.plotItem.setRange(yRange=[0, 1])
            
            # pen = pyqtgraph.mkPen(color='b')
            # self.personalPCMChart.plot(self.ear.datax, chunkData, pen=pen, clear=True)
            
            pen = pyqtgraph.mkPen(color='r')
            self.personalFFTChart.plot(self.liveProcessingEngine.getCurrentRTChunkFreq(), chunksFFT / self.maxFFT,
                                       pen=pen, clear=True)
            
            # self.pcmsChart.plot(y=list(self.staticProcessingEngine.realTimeFrequencyEnvelope), pen='r')
            self._updateFftsChart()
            # self._updatePcmsChart()
        
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
    
    def generateChooseFileDialog(self):
        filePath = QtGui.QFileDialog.getOpenFileName()
        # TODO: !!!!!!!!!!!!!!!!!!!!!!!!!
        self._drawOnce(
            chart=self.fftsChart,
            yData=self.staticProcessingEngine.calculateFrequencyEnvelope(),
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
    
    def _loopbackCheckBoxAction(self):
        if self.loopbackCheckBox.isChecked():
            self.loopbackStreamHandler.open()
            self.ear.stream.addObserver(self.loopbackStreamHandler)
        
        else:
            self.ear.stream.deleteObserver(self.loopbackStreamHandler)
            self.loopbackStreamHandler.closeOutputStream()
    
    def _updateFftsChart(self, yRange=[0, 2000]):
        
        fftsChartList = []
        staticChart = self._Chart()
        staticChart.name = "StaticChart"
        staticChart.chart = self.staticProcessingEngine.getFrequencyEnvelope()
        staticChart.color = pyqtgraph.mkPen(color='r', width=2, cosmetic=True)
        liveChart = self._Chart()
        liveChart.chart = list(self.liveProcessingEngine.realTimeFrequencyEnvelope)
        liveChart.color = pyqtgraph.mkPen(color='g', width=2)
        liveChart.name = "LiveChart"
        fftsChartList.append(staticChart)
        fftsChartList.append(liveChart)
        
        self.fftsChart.setRange(yRange=yRange)
        self.fftsChart.plotItem.clear()
        for chart in fftsChartList:
            if not hasattr(chart, "xValues"):
                chart.xValues = None
            self.fftsChart.plot(x=chart.xValues, y=chart.chart, pen=chart.color, title="FFTs Chart")
    
    def _updatePcmsChart(self):
        pass
        # self.pcmsChart.plot(y=self.liveProcessingEngine.fullAudioData, pen='b')
    
    def _drawOnce(self, chart, yData, yRange=[0, 2000]):
        """
        :param chart: pyqtgraph object to draw on
        :return: void
        """
        # color = pyqtgraph.hsvColor(time.time() / 5 % 1, alpha=.5)
        pen = pyqtgraph.mkPen(color='r', width=2)
        
        # TODO: set coorelation between np.int16 and PyAudio data types.
        
        chart.setRange(yRange=yRange)
        chart.plot(y=yData, pen=pen, clear=True)
    
    def _getLastNSeconds(self, data):
        return
    
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.UPDATE_PCM_CHART: self._updatePcmsChart(),
        }[msgType]
