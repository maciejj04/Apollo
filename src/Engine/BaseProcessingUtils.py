import numpy as np

class BaseProcessingUtils:

    def __init__(self):
        pass

    def getFFT(self, data, rate):
        """Given some data and rate, returns FFTfreq and FFT (half)."""
        data = data * np.hamming(len(data))
        fft = np.fft.fft(data)
        fft = np.abs(fft)
        # fft=10*np.log10(fft)
        freq = np.fft.fftfreq(len(fft), 1.0 / rate)
        # plt.plot(freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)])
        # plt.show()
        return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


    def getHighestFrequency(self, data):
        pass

    def findLoudestFrequency(self, list):  # arg type has to be regular (non numpy type) list
        max = 0
        for x in range(0, len(list)):
            if list[x] > max:
                max = list[x]
    
        return list.index(max)
