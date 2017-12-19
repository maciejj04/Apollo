import numpy as np
import pyqtgraph
from PyQt4 import QtGui, QtCore

from src.Commons.Audio import Audio
from src.Commons.Settings import TOP_FREQS_COUNT
from src.Engine.Ear import Ear
from src.Engine.InterpretEngine import InterpretEngine
from src.Engine.ProcessingEngine import ProcessingEngine
from src.Engine.RecordingController import Recording
from src.Engine.StaticAudio import StaticAudio
from src.MessageServer import MessageServer, MsgTypes
from src.StreamHandlers.OutputStream import OutputStream
from src.UI import MainWindow
from src.UI.ChooseMicrophoneView import ChooseMicrophoneView


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
        MessageServer.registerForEvent(self, MsgTypes.NEW_RECORDING)
        
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
        self.staticAudio = StaticAudio(rawData=rawInputAudioData)
        from src.Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel
        PluginAbstractModel.staticAudioRawData = self.staticAudio.rawData
        self.processingEngine = ProcessingEngine(staticAudio=self.staticAudio)
        self.interpretEngine = InterpretEngine(staticAudioRef=self.staticAudio)
        self.processingEngine.addObserver(self.interpretEngine)
        
        self.ear.stream.addObserver(self.processingEngine)
        self.loopbackStreamHandler = OutputStream(staticAudio=self.staticAudio)
        
        # charts Initialization
        liveFreqsEnvelopes = []
        for i in range(0, TOP_FREQS_COUNT):
            liveFreqsEnvelopes.append([])
        self.freqChartsWidget = self._ChartWidget({"orgEnvelope": 'r', "liveFreqsEnvelope": 'b'}, yValues={
            "orgEnvelope": self.processingEngine.staticAudio.nfrequencyEnvelopes,
            "liveFreqsEnvelope": liveFreqsEnvelopes
        })
        self.pcmChartWidget = self._ChartWidget({"orgEnvelope": "r", "livePcmEnvelope": "b", "averagedEnvelope": "g"}, yValues={
            "averagedEnvelope": self.staticAudio.absolutePCMEnvelope,
            "orgEnvelope": self.staticAudio.rawData,  # ???
            "livePcmEnvelope": []
        })
        
        self.pcmsChart.plot(y=self.pcmChartWidget.yValuesDict["orgEnvelope"], pen='r')
        self.pcmsChart.plot(y=self.pcmChartWidget.yValuesDict["averagedEnvelope"], pen='g')
        # self.pcmsChart.plot(y=self.pcmChartWidget.yValuesDict["orgEnvelope"], pen='b')
        
        self.plotStaticAudioFrequencyEnvelope()
        
        self.ear.stream_start()  # TODO: Do I need this here?
        self.shouldUpdatePersonalFFTChart = False
        self.shouldUpdateFrequenciesChart = False
        self.shouldUpdatePcmChart = False
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

            # self.personalFFTChart.plot(self.currentChunk.chunkFreqs,
            #                            self.currentChunk.chunkAS / self.currentChunk.chunksMaxFreq,
            #                            pen='r', clear=True)
            self.personalFFTChart.plot(self.currentChunk.chunkFreqs,
                                       self.currentChunk.rawFFT / np.max(self.currentChunk.rawFFT),
                                       pen='b', clear=True)

            self.shouldUpdatePersonalFFTChart = False
        
        if self.shouldUpdateFrequenciesChart:
            for key, values in self.freqChartsWidget.yValuesDict.items():
                for v in values:
                    self.fftsChart.plot(x=self.freqChartsWidget.xValues, y=v, pen=self.freqChartsWidget.pens[key])
            self.shouldUpdateFrequenciesChart = False
        
        if self.shouldUpdatePcmChart:
            for key, value in self.pcmChartWidget.yValuesDict.items():
                self.pcmsChart.plot(x=self.pcmChartWidget.xValues, y=value, pen=self.pcmChartWidget.pens[key])
            self.shouldUpdatePcmChart = False
        
        # import threading
        # print("Active threads: %d" % threading.activeCount())
        
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
    
    def generateChooseFileDialog(self):
        filePath = QtGui.QFileDialog.getOpenFileName()
        # TODO: Set file as staticFile
        # TODO: update and re-draw StaticAudio
        # self._drawOnce(
        #     chart=self.fftsChart,
        #     yData=self.processingEngine.calculateFrequencyEnvelopeFromRawData(),
        #     #  (min, max) = self.liveProcessingEngine.calculateMinMaxFrequencies()
        #     yRange=[0, 2000]
        # )
    
    def startButtonAction(self):
        print('StartAction')
    
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
        
        for key, values in chartsFreqs.items():
            for i in range(0, len(values)):
                self.freqChartsWidget.yValuesDict[key][i].append(values[i])
        
        self.HzLcd.display(chartsFreqs["liveFreqsEnvelope"][0])  # [0]???
        self.shouldUpdateFrequenciesChart = True
    
    def _updatePcmsChart(self):
        self.shouldUpdatePcmChart = True
    
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
    
    def _cleanUpFrequenciesChart(self, data):
        for envelope in self.freqChartsWidget.yValuesDict["liveFreqsEnvelope"]:
            envelope.clear()
        
        self.fftsChart.plotItem.clear()
        self.plotStaticAudioFrequencyEnvelope()
    
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.UPDATE_PCM_CHART: self._updatePcmsChart,
            MsgTypes.UPDATE_FREQ_SPECTR_CHART: self._updateFreqSpectrumChart,
            MsgTypes.UPDATE_FREQS_CHART: self._updateFrequenciesChart,
            MsgTypes.NEW_RECORDING: self._cleanUpFrequenciesChart
        }[msgType](data)
    
    def _updateFreqSpectrumChart(self, chunk):
        if self.listen.isChecked():
            self.currentChunk = chunk  # workaround for now, use slots/signals mechanism in future
            self.shouldUpdatePersonalFFTChart = True
            return
        return
    
    def plotStaticAudioFrequencyEnvelope(self):
    
        c = ['r', 'g', 'b']
        i = 0
        for envelope in self.processingEngine.staticAudio.nfrequencyEnvelopes:
            # C = pyqtgraph.hsvColor(time.time() / 5 % 1, alpha=.5)
            pen = pyqtgraph.mkPen(color=c[i], width=2)
            self.fftsChart.plot(envelope, pen=c[i])
            i += 1
