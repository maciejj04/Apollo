from PyQt4 import QtGui, QtCore
from Ear import Ear
import pyqtgraph
import ui_main
import numpy as np

class App(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.personalFFTChart.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 0
        self.ear = Ear(rate=44100, updatesPerSecond=100)
        self.ear.stream_start()
        
        self.fileFFTChart.plotItem.showGrid(True, True, 0.7)
    
    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax = np.max(np.abs(self.ear.data))
            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.personalPCMChart.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(self.ear.fft) > self.maxFFT:
                self.maxFFT = np.max(np.abs(self.ear.fft))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.personalFFTChart.plotItem.setRange(yRange=[0, 1])
            
            pen = pyqtgraph.mkPen(color='b')
            self.personalPCMChart.plot(self.ear.datax, self.ear.data, pen=pen, clear=True)
            
            pen = pyqtgraph.mkPen(color='r')
            self.personalFFTChart.plot(self.ear.fftx, self.ear.fft / self.maxFFT, pen=pen, clear=True)
        
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat
