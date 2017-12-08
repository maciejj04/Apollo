import numpy as np

from src.Engine.Factory import Factory


class BaseProcessingUtils:
    factory = Factory()
    
    @classmethod
    def getAplitudeSpectrum(cls, data, rate):
        """Given some data and rate, returns FFTfreq and FFT (half)."""
        data = data * np.hamming(len(data))  # TODO: Give user a choice!
        fft = np.fft.fft(data)
        # fft=10*np.log10(fft)
        freq = np.fft.fftfreq(len(fft), 1.0 / rate)
        
        notFiltered = abs(fft)
        FS = abs(cls.factory.getButterworthFilter().filter(fft))  # Filtered FrequencySpectrum
        
        return freq[:int(len(freq) / 2)], FS[:int(len(FS) / 2)], notFiltered[:int(len(notFiltered) / 2)]
