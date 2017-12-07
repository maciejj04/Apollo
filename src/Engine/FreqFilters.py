import numpy as np
from scipy.signal import butter, lfilter

class BandFilters:
    @staticmethod
    def butterworthBandPassFiler(data: np.ndarray, lowCut, highCut, fs, order=6):
        nyq = 0.5 * fs
        low = lowCut / nyq
        high = highCut / nyq
        b, a = butter(order, [low, high], btype='band')
        
        y = lfilter(b, a, data)
        return y