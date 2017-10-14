import struct
import numpy as np
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from typing import Tuple


class InterpretEngine:
    minFrequency: int = None
    maxFrequency: int = None
    
    data = None
    fft = None
    freqs = None
    
    def __init__(self, data: np.ndarray):
        """
        :param data: data in np.array return format form
        """
        self.data = data
        self.fft = np.fft.fft(self.data)
        self.freqs = np.fft.fftfreq(len(self.fft))
    
    def findHighestFreq(self, startFrame: int = 0, endFrame: int = Cai.numberOfFrames) -> int:
        """
        :return: highestFrequency in hertz
        """
        # data = struct.unpack('{n}h'.format(n=Cia.numberOfFrames), data)
        # data = np.array(data)

        # print("min, max freqs found = ({0},{1})".format(self.calculateMinMaxFrequencies(self.freqs)))
        
        # Find the peak in the coefficients
        idx = np.argmax(np.abs(self.fft[startFrame:endFrame]))
        freq = self.freqs[idx]
        freq_in_hertz = abs(freq * Cai.frameRate)
        return freq_in_hertz
    
    def calculateMinMaxFrequencies(self, freqs: np.ndarray=None) -> Tuple[int, int]:
        """
        :param freqs: data after fft->fftfreq (numpy)
        :return: tuple with (minFreq, maxFreq)
        """
        if freqs is None:
            freqs = self.freqs
        return abs(freqs.min() * Cai.frameRate), abs(freqs.max() * Cai.frameRate)
    
    def setCommonFileMinMaxFrequencies(self, freqs: Tuple[int, int]):
        """
        :param freqs: (min, max)
        :return: void
        """
        self.minFrequency = freqs[0]
        self.maxFrequency = freqs[1]
    
    def compute(self):
        pass
