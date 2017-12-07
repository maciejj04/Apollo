import numpy as np
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

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

        from src.Engine.FreqFilters import BandFilters
        fft = BandFilters.butterworthBandPassFiler(fft, 20, 18000, Cai.frameRate, order=3)
        fft = abs(fft)

        return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]
