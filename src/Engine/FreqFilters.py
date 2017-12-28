import numpy as np
from scipy.signal import butter, lfilter, freqz
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

class BandFilters:
    class ButterWorthFilter:
        def __init__(self, lowCut, highCut, order=3):
            self.nyq = 0.5 * Cai.frameRate
            self.low = lowCut / self.nyq
            self.high = highCut / self.nyq

            self.butter = butter(order, [self.low, self.high], btype='bandpass')  # TODO: can be cached!!!
        
        def filter(self, data: np.ndarray):
            y = lfilter(self.butter[0], self.butter[1], data)
            return y


def butter_bandpass(lowcut, highcut, fs, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import wave
    Cai.frameRate = 44100
    order=3

    bf = BandFilters.ButterWorthFilter(18, 18000, order=order).butter
    w2, h2 = freqz(bf[0], bf[1], worN=4410)

    #BandFilters.ButterWorthFilter().butter
    
    fs = 44100
    b, a = butter_bandpass(18, 18000, fs, order=order)
    w, h = freqz(b, a)
    plt.plot(
#        abs(h2), 'b',
        abs(h), 'r'
        )

    f = wave.open("../../resources/osiem1.wav")
    x = f.readframes(f.getnframes())  # Raw audio data (in bytes)
    x = np.fromstring(x, dtype=np.int16)

    plt.show()
    
    