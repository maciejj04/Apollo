import pyqtgraph

from src.tools.helper_functions import *
from src.Engine.InterpretEngine import InterpretEngine


def drawOnce(wave, chart):
    """
    :param wave: object that wave.open() returns
    :param chart: pyqtgraph object to draw on
    :return: void
    """
    # color = pyqtgraph.hsvColor(time.time() / 5 % 1, alpha=.5)
    pen = pyqtgraph.mkPen(color='r', width=2)
    
    (nchannels, sampwidth, framerate, nframes, comptype, compname, updatesPerSecond) = Cai.getInformations()
    
    rawData = wave.readframes(nframes)
    wave.close()
    # Y = np.fromstring(rawData, dtype=np.int16)
    # TODO: find coorelation between np.int16 and PyAudio data types. Do We need PyAudio?
    
    freqs = []
    chunk = Cai.getChunk()
    print("chunk: %s" % chunk)
    arrayWithRawData = np.fromstring(rawData, dtype=np.int16)

    engine = InterpretEngine(arrayWithRawData)
    # print("Highest freq for whole file is %s" % engine.findHighestFreq())
    (min, max) = engine.calculateMinMaxFrequencies()
    
    i=0
    for startFrame in my_range(0, Cai.numberOfFrames-chunk, chunk):
        highestFreq = InterpretEngine.findHighestFreq(arrayWithRawData[startFrame:startFrame+chunk])
        # highestFreq = engine.findHighestFreq(startFrame=startFrame, endFrame=startFrame+chunk)
        print("{0}. Highest freq found in sample[{start},{end}] = {1}".format(i, highestFreq, start=startFrame, end=startFrame+chunk))
        freqs.append(highestFreq)
        i += 1
    
    chart.setRange(yRange=[0, max])
    chart.plot(y=freqs, pen=pen, clear=True)
