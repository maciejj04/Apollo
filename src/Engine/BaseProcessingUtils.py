import numpy as np

from src.Engine.Factory import Factory
from src.Engine.Windowing import Window
from  src.Commons.Settings import WINDOW_TYPE

class BaseProcessingUtils:
    factory = Factory()
    
    @classmethod
    def getAplitudeSpectrum(cls, data, rate):
        """Given some data and rate, returns FFTfreq and FFT (half)."""
        data = Window(WINDOW_TYPE).window(data)
        
        fft = np.fft.fft(data)
        # fft=10*np.log10(fft)
        freq = np.fft.fftfreq(len(fft), 1.0 / rate)
        
        notFiltered = abs(fft)
        FS = abs(cls.factory.getButterworthFilter().filter(fft))  # Filtered FrequencySpectrum
        
        return freq[:int(len(freq) / 2)], FS[:int(len(FS) / 2)], notFiltered[:int(len(notFiltered) / 2)]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import wave
    from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
    
    Cai.frameRate = 44100
    f = wave.open("../../resources/osiem1.wav")
    x = f.readframes(f.getnframes())  # Raw audio data (in bytes)
    x = np.fromstring(x, dtype=np.int16)
    
    import scipy
    
    fs, asf, asnf = BaseProcessingUtils.getAplitudeSpectrum(x, 44100)
    
    plt.plot(asnf, 'r', asf, 'b')
    plt.show()
