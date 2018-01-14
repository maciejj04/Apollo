import numpy as np
from scipy.signal import butter, lfilter

from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel
from scipy.signal import argrelextrema

# DO NOT USE. Not finished for now. Just scaffolder
class MaxPowerFreqPeaks(PluginAbstractModel):
    def __init__(self, windowWidth):
        super().__init__(windowWidth)
        self.divideCoefficient = 10
        self.windowSize = int(self.windowWidth / self.divideCoefficient)
    
    def process(self, data) -> str:
        windowsEnergies = []
        AS = abs(
            MaxPowerFreqPeaks
                .ButterWorthFilter(18, 18000)
                .filter(
                    np.fft.fft(data)
                )
        )
        AS = AS[:int(len(AS)/2)]
        
        chunkEnergySum = self.calculateEnegry(signal=AS)
        print("Chunk EnergySum: %d" % chunkEnergySum)
        

        print("AS len={}".format(len(AS)))

        maxPeaks = argrelextrema(AS, np.greater)
        print("Max peaks = {}, array len={}".format(maxPeaks, maxPeaks[0].size))

        c = (np.diff(np.sign(np.diff(AS))) < 0).nonzero()[0] + 1  # local max
        print("LocMax = {}, len = {}".format(c, len(c)))


        import matplotlib.pyplot as plt
        plt.plot(abs(AS))
        plt.show()
        
    def calculateEnegry(self, signal: np.ndarray):
        energy = 0
        for e in signal:
            # absolute = abs(e)  # redundant
            energy += e * e
        
        return energy / signal.size
    
    class ButterWorthFilter:
        def __init__(self, lowCut, highCut, order=3):
            from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai  # TODO: To be changed
            self.nyq = 0.5 * Cai.frameRate
            self.low = lowCut / self.nyq
            self.high = highCut / self.nyq
            
            self.butter = butter(order, [self.low, self.high], btype='bandpass')  # TODO: can be cached!!!
        
        def filter(self, data: np.ndarray):
            y = lfilter(self.butter[0], self.butter[1], data)
            return y


if __name__ == "__main__":
    Cai.frameRate = 44100
    import wave
    
    f = wave.open("../../../../resources/osiem2.wav")
    x = f.readframes(f.getnframes())  # Raw audio data (in bytes)
    x = np.fromstring(x, dtype=np.int16)
    
    m = MaxPowerFreqPeaks(windowWidth=4410)
    cut = x[0:4410]
    m.process(cut)  # np.array([1, 2, 3, 4, 5, 1, 6, 3, 7, 6, 4, 75, 7, 9, -9, 9])
    print("stop")
    
    # a = np.array([1, 2, 3, 4, 5, 1, 6, 3, 7, 6, 4, 75, 7, 9, -9, 9])
    # var = np.r_[True, a[1:] < a[:-1]] & np.r_[a[:-1] < a[1:], True]
