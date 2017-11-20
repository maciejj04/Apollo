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
from src.StreamHandlers.OutputStream import OutputStream
from src.Engine.StaticAudio import StaticAudio
from src.Engine.RecordingController import Recording
from src.Engine.LiveAudio import LiveAudio
from src.Engine.StaticAudio import StaticAudio


class App(QtGui.QMainWindow, MainWindow.Ui_MainWindow):  # , MessageClient
    class _ChartWidget:
        def __init__(self, pens: dict, xValues=None, yValues={}):
            self.xValues = xValues
            self.yValuesDict = yValues  # list of lists.
            self.pens = pens
            
        def addChart(self, name: str, yValues: list, pen):
            self.yValuesDict[name] = yValues
            self.pens[name] = pen
    
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')
        super(App, self).__init__(parent)
        MessageServer.registerForEvent(self, MsgTypes.UPDATE_PCM_CHART)
        MessageServer.registerForEvent(self, MsgTypes.UPDATE_FREQ_SPECTR_CHART)
        MessageServer.registerForEvent(self, MsgTypes.UPDATE_FREQS_CHART)
        
        self.setupUi(self)
        self.resize(1300, 900)
        self.personalFFTChart.plotItem.showGrid(True, True, 0.7)
        self.fftsChart.plotItem.showGrid(True, True, 0.7)
        self.pcmsChart.plotItem.showGrid(True, True, 0.7)
        

        self.loopbackCheckBox.stateChanged.connect(self._loopbackCheckBoxAction)
        self.startButton.clicked.connect(self.startButtonAction)
        self.listen.stateChanged.connect(self.update)
        self.actionChoose_file.triggered.connect(self.generateChooseFileDialog)
        self.actionChange_microphone.triggered.connect(self.showChooseMicrophoneDialog)
        self.recordButton.clicked.connect(self.recordButtonAction)
        self.ear = Ear()
        rawInputAudioData = Audio().loadFromPathAndAdjust().getRawDataFromWav()
        
        self.processingEngine = ProcessingEngine(staticAudio=StaticAudio(rawData=rawInputAudioData))
        self.ear.stream.addObserver(self.processingEngine)
        self.loopbackStreamHandler = OutputStream(StaticAudio(rawInputAudioData))
        
        # charts Initialization
        self.freqCharts = self._ChartWidget({"orgEnvelope": 'r', "liveFreqsEnvelope": 'b'}, yValues={
            "orgEnvelope": self.processingEngine.staticAudioFrequencyEnvelope,
            "liveFreqsEnvelope": []
        })
        
        
        # self._drawOnce(
        #     chart=self.fftsChart,
        #     yData=self.liveProcessingEngine.calculateFrequencyEnvelope(),
        #     #  (min, max) = self.liveProcessingEngine.calculateMinMaxFrequencies()
        #     yRange=[0, 2000]
        # )
        self.pcmsChart.plot(y=self.processingEngine.fullAudioData, pen='r')
        # self._updateFftsChart()
        
        self.fftsChart.plot(self.processingEngine.getStaticAudioFrequencyEnvelope(), pen='r')

        self.ear.stream_start()  # TODO: Do I need this here?
        self.shouldUpdatePersonalFFTChart = False
        self.shouldUpdateFrequenciesChart = False
        self.update()
    
    def update(self):
        
        # if not self.listen.isChecked():
        #     return
        #
        # chunksFFT = self.liveProcessingEngine.getCurrentRTChunkFFT()
        # chunkData = self.liveProcessingEngine.getCurrentRTChunk().rawData
        #
        # if chunkData is not None and chunksFFT is not None:
        # pcmMax = np.max(np.abs(chunkData))
        # if pcmMax > self.maxPCM:
        #     self.maxPCM = pcmMax
        #     self.personalPCMChart.plotItem.setRange(yRange=[-pcmMax, pcmMax])
        # if np.max(chunksFFT) > self.maxFFT:
        #     self.maxFFT = np.max(np.abs(chunksFFT))
        #     # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
        #     self.personalFFTChart.plotItem.setRange(yRange=[0, 1])
        #
        # pen = pyqtgraph.mkPen(color='b')
        # self.personalPCMChart.plot(self.ear.datax, chunkData, pen=pen, clear=True)
        
        # self.personalFFTChart.plot(self.liveProcessingEngine.getCurrentRTChunkFreq(), chunksFFT / self.maxFFT,
        #                            pen=pen, clear=True)
        #
        # self.pcmsChart.plot(y=list(self.staticProcessingEngine.realTimeFrequencyEnvelope), pen='r')
        # self._updateFftsChart()
        # self._updatePcmsChart()
        if self.shouldUpdatePersonalFFTChart is True:
            self.personalFFTChart.plot(self.currentChunk.chunkFreqs,
                                       self.currentChunk.chunkFFT / self.currentChunk.chunksMaxFreq,
                                       pen='r', clear=True)
            self.shouldUpdatePersonalFFTChart = False
            
        if self.shouldUpdateFrequenciesChart:
            #TODO: corrent! For loop every chart !
            for key, value in self.freqCharts.yValuesDict.items():
                self.fftsChart.plot(x=self.freqCharts.xValues, y=value, pen=self.freqCharts.pens[key])
                self.shouldUpdateFrequenciesChart = False

        
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
    
    def generateChooseFileDialog(self):
        filePath = QtGui.QFileDialog.getOpenFileName()
        # TODO: Set file as staticFile
        self._drawOnce(
            chart=self.fftsChart,
            yData=self.processingEngine.calculateFrequencyEnvelope(),
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
        Recording.startRecording()
    
    def _loopbackCheckBoxAction(self):
        if self.loopbackCheckBox.isChecked():
            self.loopbackStreamHandler.open()
            self.ear.stream.addObserver(self.loopbackStreamHandler)
        
        else:
            self.ear.stream.deleteObserver(self.loopbackStreamHandler)
            self.loopbackStreamHandler.closeOutputStream()
    
    def _updateFrequenciesChart(self, chartsFreqs: dict, yRange=[0, 2000]):
        
        for key, value in chartsFreqs.items():
            self.freqCharts.yValuesDict[key].append(value)
            
        self.shouldUpdateFrequenciesChart = True
        
        # self.fftsChart.setRange(yRange=yRange)
        # self.fftsChart.plotItem.clear()
        # for chart in fftsChartList:
        #     if not hasattr(chart, "xValues"):
        #         chart.xValues = None
        #     self.fftsChart.plot(x=chart.xValues, y=chart.chart, pen=chart.color, title="FFTs Chart")
    
    def _updatePcmsChart(self):
        pass
    
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
    
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.UPDATE_PCM_CHART: self._updatePcmsChart,
            MsgTypes.UPDATE_FREQ_SPECTR_CHART: self._updateFreqSpectrumChart,
            MsgTypes.UPDATE_FREQS_CHART: self._updateFrequenciesChart
        }[msgType](data)
    
    def _updateFreqSpectrumChart(self, chunk):
        if self.listen.isChecked():
            self.currentChunk = chunk  # workaround for now, use slots/signals mechanism in future
            self.shouldUpdatePersonalFFTChart = True
            return
        return
