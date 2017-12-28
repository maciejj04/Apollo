import wave

import numpy as np


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
        #meanedEnvelope = self.meanN(maxEnvelope, meanWindowSize)
        meanedEnvelope = self.meanWithIgnoredBegin(maxEnvelope, meanWindowSize)
        
        return meanedEnvelope


if __name__ == "__main__":
    f = wave.open("../../../../resources/osiem1.wav")
    import matplotlib.pyplot as plt
    
    x = f.readframes(f.getnframes())  # Raw audio data (in bytes)
    x = np.fromstring(x, dtype=np.int16)
    
    envelope = Envelope(windowSize=200).threeStepEnvelope(x, meanWindowSize=200)
    
    plt.plot(abs(x), 'r', envelope, 'b')
    plt.show()
