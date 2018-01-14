import wave

import numpy as np

from Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel
from Engine.PluginPackage.plugins.EnvelopesCorrelation import EnvelopesCorrelation
from Engine.PluginPackage.plugins.StaticCorrPlugin import StaticCorrPlugin
from MessageServer import MsgTypes


def squareSum(dataSet):
    return sum(e * e for e in dataSet)


class Envelope:
    def __init__(self, windowSize: int):
        self._windowSize: int = windowSize
    
    def meanWithIgnoredBegin(self, signal: np.ndarray, windowSize: int = None) -> np.ndarray:
        # mean should skips beginning
        if windowSize is None:
            windowSize = self._windowSize
        
        filtered = []
        gapSize = int(windowSize / 2)
        
        gapMean = np.mean(signal[0: gapSize])
        for i in range(gapSize):
            filtered.append(gapMean)
        
        for i in range(0, signal.size, 1):
            filtered.append(
                np.mean(signal[i:i + windowSize])
            )
        
        return filtered
    
    def meanN(self, signal: np.ndarray, windowSize: int = None):
        # mean should skips beginning and end
        if windowSize is None:
            windowSize = self._windowSize
        
        filtered = []
        for i in range(0, signal.size, 1):
            filtered.append(
                np.mean(signal[i:i + windowSize])
            )
        
        return filtered
    
    def maxEnvelope(self, signal: np.ndarray) -> np.array:
        envelope = []
        for i in range(0, signal.size, 1):
            envelope.append(
                np.max(signal[i:i + self._windowSize])
            )
        
        return np.array(envelope)
    
    def threeStepEnvelope(self, signal: np.ndarray, meanWindowSize) -> np.array:
        # 1
        signal = abs(signal)
        # 2
        maxEnvelope = self.maxEnvelope(signal)
        # 3
        # meanedEnvelope = self.meanN(maxEnvelope, meanWindowSize)
        meanedEnvelope = self.meanWithIgnoredBegin(maxEnvelope, meanWindowSize)
        
        return meanedEnvelope


if __name__ == "__main__":
    f = wave.open("../../../../resources/osiem1.wav")
    f2 = wave.open("../../../../resources/osiem2.wav") # sweep_230Hz_330Hz_-3dBFS_1s
    import matplotlib.pyplot as plt
    
    o1 = np.fromstring(f.readframes(f.getnframes()), dtype=np.int16)
    o2 = np.fromstring(f2.readframes(f2.getnframes()), dtype=np.int16)
    
    envelope = Envelope(windowSize=200).threeStepEnvelope(o1, meanWindowSize=200)
    envelope2 = Envelope(windowSize=200).threeStepEnvelope(o2, meanWindowSize=200)
    from scipy import stats, sqrt
    
    print("Pearson coefficient = {}".format(
        stats.pearsonr(envelope, envelope2)[0]))  # TODO: evaluate second return-tuple element!
    corrObj = StaticCorrPlugin.NormalizedCrossCorr(envelope)
    corr = corrObj.measureNormalizedCrossCorelation(envelope, envelope2)
    
    print("MyCorr = {}".format(corr))
    
    # corr picture
    corrObj = EnvelopesCorrelation(env1=envelope, env2=envelope2, windowSize=25181)
    corrObj.correlate()
    
    plt.plot(o2, 'r', envelope, 'g', envelope2, 'b')
    plt.show()
