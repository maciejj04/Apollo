from PyQt4 import QtGui, QtCore
import sys
import ui_main
import pyqtgraph
import time
import ui_main
from ReadFile import readFile
import numpy as np
from helper_functions import *
from Ear import Ear


def drawOnce(chart):
    color = pyqtgraph.hsvColor(time.time() / 5 % 1, alpha=.5)
    pen = pyqtgraph.mkPen(color=color, width=1)
    
    if len(sys.argv) < 2:
        data = readFile('./resources/tone.wav')
    else:
        data = readFile(sys.argv[1])
        
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = data.getparams()
    
    nrOfFrames = data.getnframes()
    frames = data.readframes(nrOfFrames)
    X = np.arange(nrOfFrames)  # np.arange(data.getnframes())
    Y = np.fromstring(frames, dtype=np.int8)
    
    print('''You choose : {}\t -
                    nrOfFrames: {}'''.format(sys.argv[0], nrOfFrames))
    
    maxFFTvalues = []
    for x in my_range(0, nrOfFrames - 100, 100):
        # print('%d  '%x)
        fftx, values = getFFT(Y[x:x + 15], framerate)
        maxFFTvalues.append(np.max(values))
        # print("values %s" %values)

    # print("%s" % maxFFTvalues)
    
    chart.plot(x=np.arange(len(maxFFTvalues)), y=maxFFTvalues, pen=pen, clear=True)
    data.close()


class App(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.personalFFTChart.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 0
        self.ear = Ear(rate=44100, updatesPerSecond=20)
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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = App()
    form.show()
    drawOnce(form.fileFFTChart)
    form.update()
    #form.update()  # start with something
    app.exec_()
    print("DONE")
