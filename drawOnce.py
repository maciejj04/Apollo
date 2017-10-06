import sys
import pyqtgraph
import time
from ReadFile import readFile
import numpy as np
from helper_functions import *
from CommonAudioInfo import CommonAudioInfo
from Audio import Audio

def drawOnce(data, chart):
    # color = pyqtgraph.hsvColor(time.time() / 5 % 1, alpha=.5)
    pen = pyqtgraph.mkPen(color='r', width=2)
    
    ( nchannels, sampwidth, framerate, nframes, comptype, compname ) = Audio.getInformations()
   
    #framerate -> CommonAudioInfo.frameRate. After unifying audio format
    chunk = int(framerate / CommonAudioInfo.updatesPerSecond)  # nr of frames for getFFT() invocation
    frames = data.readframes(nframes)
    Y = np.fromstring(frames, dtype=np.int8)
    
 
    maxFFTvalues = []
    # for x in my_range(0, nrOfFrames - chunk, chunk):
    print("chunk: %s" % Y.size)
    fftx, values = getFFT(Y[0:15], framerate)
    # print(fftx)
    # print(values)
    #    maxFFTvalues.append(np.max(values))
    
    print(values[-1000:-900].mean())
    chart.plot(fftx, y=values, pen=pen, clear=True)
    data.close()