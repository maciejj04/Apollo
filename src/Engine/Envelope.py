import wave

import numpy as np


class Envelope:
    def __init__(self, windowSize: int):
        self._windowSize: int = windowSize
    
    def _meanWithIgnoredBegin(self, signal: np.ndarray, windowSize: int = None) -> np.ndarray:
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
    
    def _maxEnvelope(self, signal: np.ndarray) -> np.array:
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
        maxEnvelope = self._maxEnvelope(signal)
        # 3
        meanedEnvelope = self._meanWithIgnoredBegin(maxEnvelope, meanWindowSize)
        
        return meanedEnvelope
