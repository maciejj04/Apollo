from functools import wraps

import numpy as np
from math import sqrt

from src.Engine.PluginModule.PluginAbstractModel import PluginAbstractModel
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
import time

from src.MessageServer import MsgTypes


def timer(func):
    @wraps(func)
    def timeFunc(*args, **kwargs):
        st = time.time()
        res = func(*args, **kwargs)
        processingTime = time.time() - st
        
        print("Method {mthName} took {time}".format(mthName=func.__name__, time=processingTime))
        
        return res
    
    return timeFunc


class StaticCorrPlugin(PluginAbstractModel):
    """
    Plugin finds best fit for chunks spectrum in static audio. It is implemented by using 'moving' window.
    'Step' for the moving window is 1/10 of a window length - this is determined by computing power of device that
    application runs on. As an effect class produces vector of correlation for each window => vector of vectors.
    This is to find delays and tempo change in user version of the recording.
    This version of CorrPlugin analyses twa audio files "offline" so, after the recording ended.
    This is due to big CPU load during RT analysis by live plugin version (CorrPlugin).
    In the future Plugin (or all of the plugins) should be considered for running in separete processes by reason of GIL.
    """
    
    # WARN! No bandpass filter for now!
    def __init__(self, windowWidth):
        super().__init__(windowWidth)
        self.corrValues: [] = []
        self.step: int = int(
            self.windowWidth / 10)  # TODO: Hardcoded for now. Should be set according to the application flow.
        self.staticSpectrums: [] = []
        self.liveSpectrums: [] = []
        self.liveAudioRawData: np.ndarray = np.array([])  # assume that type is float64?
        self.startIndex: int = 0
        self.correlationVectors: [] = []
        self.staticSpectrums = self.processSpectrumsFromRawData(self.staticAudioRawData)
    
    def process(self, data) -> str:
        self.liveAudioRawData = np.append(self.liveAudioRawData, data)
        return "StaticCorrPlugin appended data"
    
    # one object per single window analysis
    class NormalizedCrossCorr:
        def __init__(self, data1):
            self.squareSumSqrt = sqrt(squareSum(data1))
        
        def measureNormalizedCrossCorelation(self, data1: np.ndarray, data2: np.ndarray):
            return np.correlate(data1, data2)[0] / \
                   (self.squareSumSqrt * sqrt(squareSum(data2)))
    
    def processSpectrumsFromRawData(self, data: np.ndarray):
        spectrums = []
        for i in range(0, data.size - self.windowWidth, self.step):
            spectrums.append(
                self._getFreqSpectrum(
                    data[i: i + self.windowWidth]
                )
            )
        
        return spectrums
    
    def _getFreqSpectrum(self, data: np.ndarray) -> np.ndarray:
        data = data * np.hamming(len(data))  # TODO: Give user a choice!
        freqSpectrum = abs(np.fft.fft(data))  # Can be optimized
        
        return freqSpectrum[:int(len(freqSpectrum) / 2)]
    
    @timer
    def _compareWithEachStaticSpectrum(self, spectrum: np.ndarray):
        corr = StaticCorrPlugin.NormalizedCrossCorr(spectrum)
        corrVector = []
        for j in range(0, len(self.staticSpectrums)):
            print("StaticSpectrums[{}]".format(j))
            corrVector.append(
                corr.measureNormalizedCrossCorelation(
                    spectrum, self.staticSpectrums[j]
                )
            )
        return corrVector
    
    def correlateSoundTracks(self):
        print("LiveSpectrums len = %d" % len(self.liveSpectrums))
        for i in range(0, len(self.liveSpectrums), 1):
            print("Corr with LiveSpectrums[{}]".format(i))
            self.correlationVectors.append(
                self._compareWithEachStaticSpectrum(self.liveSpectrums[i])
            )
    
    def handleMessage(self, msgType, data):
        if msgType.value[0] == 4:
            self.liveSpectrums = self.processSpectrumsFromRawData(self.liveAudioRawData)
            self.correlateSoundTracks()
            #self.dropCorrVectorsToFile()
            #self.print3DPlot(self.correlationVectors)
    
    def print3DPlot(self, arrayOfArrays):
        import matplotlib.pyplot as plt
        im = plt.imshow(arrayOfArrays, cmap='hot')
        plt.colorbar(im, orientation='horizontal')
        plt.show()

    def dropCorrVectorsToFile(self, filePath="./logs/corrValues.txt"):
        f = open(filePath, 'w')
        for e in self.correlationVectors:
            for i in e:
                f.write(str(i))
        f.close()
        


def squareSum(dataSet):
    return sum(e * e for e in dataSet)


if __name__ == "__main__":
    # sweep_220Hz_440Hz_ - 3dBFS_2s
    import wave
    
    f1 = wave.open("../../../../resources/whistle1.wav")#  sweep_220Hz_330Hz_-3dBFS_1s
    f2 = wave.open("../../../../resources/whistle2.wav")#  sweep_255Hz_330Hz_-3dBFS_1s
    rawData1 = np.fromstring(f1.readframes(f1.getnframes()), dtype=np.int16)
    rawData2 = np.fromstring(f2.readframes(f2.getnframes()), dtype=np.int16)
    PluginAbstractModel.staticAudioRawData = rawData1
    s = StaticCorrPlugin(windowWidth=4410)
    s.liveAudioRawData = rawData2
    s.handleMessage(msgType=MsgTypes.RECORDING_STOP, data="mock")
    s.dropCorrVectorsToFile(filePath="./corrVectors.txt")
