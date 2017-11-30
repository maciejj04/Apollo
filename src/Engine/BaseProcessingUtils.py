import numpy as np

class BaseProcessingUtils:

    def __init__(self):
        pass

    @staticmethod
    def getAplitudeSpectrum(data, rate):
        """Given some data and rate, returns FFTfreq and FFT (half)."""
        #data = data * np.hamming(len(data))#TODO: should give a choice to user?
        fft = np.abs(np.fft.fft(data))
        # fft=10*np.log10(fft)
        freq = np.fft.fftfreq(len(fft), 1.0 / rate)

        return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]
