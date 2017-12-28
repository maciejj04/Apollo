import wave

import numpy as np

from src.Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel
from scipy.signal import butter, lfilter, freqz
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


# DO NOT USE. Not finished for now. Just scaffolder
class MaxPowerFreqPeaks(PluginAbstractModel):
    def __init__(self, windowWidth):
        super().__init__(windowWidth)
        self.divideCoefficient = 10
        self.windowSize = int(self.windowWidth / self.divideCoefficient)
    
    def process(self, data) -> str:
        return
        windowsEnergies = []
        AS = abs(MaxPowerFreqPeaks.ButterWorthFilter(18, 18000).filter(np.fft.fft(data)))
        chunkEnergySum = self.calculateEnegry(signal=AS)
        print("Chunk EnergySum: %d" % chunkEnergySum)
        
        import matplotlib.pyplot as plt
        plt.plot(abs(AS))
        plt.show()
        
        for i in range(0, AS.size - self.windowSize + 1, self.windowSize):
            windowsEnergies.append(
                self.calculateEnegry(AS[i:i + self.windowSize])
            )
        plt.plot(windowsEnergies)
        plt.show()
    
    def calculateEnegry(self, signal: np.ndarray):
        energy = 0
        for e in signal:
            absolute = abs(e)  # redundant
            energy += absolute * absolute
        
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
    
    f = wave.open("../../../../resources/440_1s.wav")
    x = f.readframes(f.getnframes())  # Raw audio data (in bytes)
    x = np.fromstring(x, dtype=np.int16)
    
    m = MaxPowerFreqPeaks(windowWidth=4410)
    cut = x[0:4410]
    m.process(cut)  # np.array([1, 2, 3, 4, 5, 1, 6, 3, 7, 6, 4, 75, 7, 9, -9, 9])
    print("stop")
    
    a = np.array([1, 2, 3, 4, 5, 1, 6, 3, 7, 6, 4, 75, 7, 9, -9, 9])
    var = np.r_[True, a[1:] < a[:-1]] & np.r_[a[:-1] < a[1:], True]
