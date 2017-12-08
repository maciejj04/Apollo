import numpy as np
from scipy.signal import butter, lfilter
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

class BandFilters:
    class ButterWorthFilter:
        def __init__(self, lowCut, highCut, order=3):
            self.nyq = 0.5 * Cai.frameRate
            self.low = lowCut / self.nyq
            self.high = highCut / self.nyq

            self.butter = butter(order, [self.low, self.high], btype='band')  # TODO: can be cached!!!
        
        def filter(self, data: np.ndarray):
            y = lfilter(self.butter[0], self.butter[1], data)
            return y
