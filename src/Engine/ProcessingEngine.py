from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from typing import Tuple
import numpy as np

# def checkParametersBeforeCall(func):
#     def funcWrapper():
# from functools import wraps

# def checkClassVariable(*classVars):
#     for v in classVars:
#         if v is None:
#             return
#
#     def tagDecorator(func):
#         @wraps(func)
#         def funcWrapper(*args):
#             if args is not None:
#                 func(*args)
#
#         return funcWrapper
#     return tagDecorator

class ProcessingEngine(BaseProcessingUtils):
    """
        class can work in state-full or state-less mode(?)
        Real Time analysis possibilites:
            - FFT
            - min/max freq of a sample

    """
    datax = None
    
    fullAudioData: np.ndarray = None
    fullAudioFFT: np.ndarray = None
    fullAudioFreqs: np.ndarray = None
    
    minFrequency: int = None
    maxFrequency: int = None
    
    chunksMinFreq: list = []
    chunksMaxFreq: list = []
    
    chunksFFT: np.ndarray = None
    chunksFreqs: np.ndarray = None
    
    currentChunkData: np.ndarray = None
    
    def __init__(self, data: np.ndarray = None):
        super().__init__()
        """
        :param data: data in np.array return format form
        """

        if data is None:
            return

        self.fullAudioData = data
        self.fullAudioFreqs, self.fullAudioFFT = self.getFFT(data, Cai.frameRate)
    
    # def calculateFFTAndFreqs(self, data=None):
    #     if data is None:
    #         data = self.fullAudioData
    #     self.fft = np.fft.fft(data)
    #     self.freqs = np.fft.fftfreq(len(self.fft))
    
    def withData(self, data):
        self.data = data
        return self
    
    def findHighestFreq(self, startFrame: int = 0, endFrame: int = Cai.numberOfFrames) -> int:
        """
        :return: highestFrequency in hertz
        """
        # data = struct.unpack('{n}h'.format(n=Cia.numberOfFrames), data)
        # data = np.array(data)
        
        # print("min, max freqs found = ({0},{1})".format(self.calculateMinMaxFrequencies(self.freqs)))
        
        # Find the peak in the coefficients
        idx = np.argmax(np.abs(self.fft[startFrame:endFrame]))
        freq = self.fullAudioFreqs[startFrame + idx]
        freq_in_hertz = abs(freq * Cai.frameRate)
        return freq_in_hertz
    
    def calculateMinMaxFrequencies(self, freqs: np.ndarray = None) -> Tuple[int, int]:
        """
        :param freqs: data after fft->fftfreq (numpy)
        :return: tuple with (minFreq, maxFreq)
        """
        if freqs is None:
            freqs = self.fullAudioFreqs
        return abs(freqs.min() * Cai.frameRate), abs(freqs.max() * Cai.frameRate)
    
    @staticmethod
    def findHighestFreq(data: np.ndarray) -> int:
        """
        :return: highestFrequency in hertz
        """
        
        fft = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(fft))
        
        idx = np.argmax(np.abs(fft))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * Cai.frameRate)
        return freq_in_hertz
    
    def calculateEnvelope(self):  # obwiednia
        # caluculates envelope based on full Audio PCM signal.
        pass
    
    # TODO: ......................
    # def maxFrequency(X, F_sample, Low_cutoff=80, High_cutoff=300):
    #     """ Searching presence of frequencies on a real signal using FFT
    #     Inputs
    #     =======
    #     X: 1-D numpy array, the real time domain audio signal (single channel time series)
    #     Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
    #     High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
    #     F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
    #     """
    #
    #     M = X.size  # let M be the length of the time series
    #     Spectrum = sf.rfft(X, n=M)
    #     [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])
    #
    #     # Convert cutoff frequencies into points on spectrum
    #     [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])
    #
    #     maximumFrequency = np.where(
    #         Spectrum == np.max(Spectrum[Low_point: High_point]))  # Calculating which frequency has max power.
    #
    #     return maximumFrequency
    def setCommonFileMinMaxFrequencies(self, freqs: Tuple[int, int]):
        """
        :param freqs: (min, max)
        :return: void
        """
        self.minFrequency = freqs[0]
        self.maxFrequency = freqs[1]

    
    # Used by observer pattern!

    def handleNewData(self, data):
        self.fftx, self.fft = self.getFFT(data, Cai.frameRate)
