from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.tools.helper_functions import my_range
from typing import Tuple
from src.Observer import Observer
import numpy as np
from src.Engine.Chunk import Chunk
from collections import deque
from src.MessageClient import MessageClient
from src.MessageServer import MessageServer, MsgTypes


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

class ProcessingEngine(BaseProcessingUtils, Observer, MessageClient):
    """
        class can work in state-full or state-less mode(?)
        Real Time analysis possibilites:
            - TODO
    """
    
    datax = None  # TODO: not used yet. For now datax is in Ear
    
    fullAudioData: np.ndarray = None
    fullAudioFFT: np.ndarray = None
    fullAudioFreqs: np.ndarray = None
    frequencyEnvelope: list = None
    PCMEnvelope: np.ndarray = None
    
    minFrequency: int = None
    maxFrequency: int = None
    
    recordChunks: list = []
    realTimeChunks: deque = None  # deque(maxlen=Cai.numberOfFrames)
    realTimeFrequencyEnvelope: deque = None  # deque(maxlen=Cai.numberOfFrames)
    realTimePCMEnvelope: deque = None  # deque(maxlen=Cai.numberOfFrames)
    
    currentChunkNr: int = -1
    recording = False
    
    def __init__(self, data: np.ndarray = None):
        """
        :param data: data in np.array return format form
        """
        Observer.__init__(self)
        MessageServer.register(self)  # TODO: change to registerForEvent
        
        self.realTimeChunks = deque(maxlen=Cai.numberOfFrames)
        self.realTimeFrequencyEnvelope = deque(maxlen=Cai.numberOfFrames)
        self.realTimePCMEnvelope = deque(maxlen=Cai.numberOfFrames)
        
        if data is None:
            self.fullAudioData = np.ones(0, dtype=Cai.sampleWidthNumpy)
            return
        
        self.fullAudioData = data
        self.fullAudioFreqs, self.fullAudioFFT = self.getFFT(data, Cai.frameRate)
    
    def withData(self, data):
        self.data = data
        return self
    
    def getFrequencyEnvelope(self):
        return self.calculateFrequencyEnvelope() if self.frequencyEnvelope is None else self.frequencyEnvelope
    
    def calculateFrequencyEnvelope(self, rawDataArray=None):
        if rawDataArray is None:
            rawDataArray = self.fullAudioData
        chunk = Cai.getChunkSize()
        freqs = []
        i = 0
        for startFrame in my_range(0, Cai.numberOfFrames - chunk, chunk):
            highestFreq = ProcessingEngine.findHighestFreqFromRawData(rawDataArray[startFrame:startFrame + chunk])
            # highestFreq = engine.findHighestFreq(startFrame=startFrame, endFrame=startFrame+chunk)
            print("{0}. Highest freq found in sample[{start}:{end}] = {1}".format(i, highestFreq, start=startFrame,
                                                                                  end=startFrame + chunk))
            freqs.append(highestFreq)
            i += 1
        
        self.frequencyEnvelope = freqs
        return freqs
    
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
    def findHighestFreqFromRawData(data: np.ndarray) -> int:
        """
        :return: highestFrequency in hertz
        """
        freq, fft = BaseProcessingUtils.getFFT(data, Cai.frameRate)
        return ProcessingEngine.findHighestFreqFromFFT(fft, freq)
    
    @staticmethod
    def findHighestFreqFromFFT(fftData: np.ndarray, freqs=None) -> int:
        if freqs is None:
            freqs = np.fft.fftfreq(len(fftData))
        
        idx = np.argmax(np.abs(fftData))
        freq = freqs[idx]
        freq_in_hertz = abs(freq)  # * Cai.frameRate)
        return freq_in_hertz
    
    def calculatePCMEnvelope(self, data=None):  # obwiednia
        if data is None:
            data = self.fullAudioData
        
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
    
    
    # Used by observer pattern!
    
    def handleNewData(self, data, shouldSave=False):
        self.currentChunkNr += 1
        chunk = Chunk(data, self.currentChunkNr)
        self.realTimeChunks.append(chunk)
        
        if shouldSave:
            self.recordChunks.append(chunk)
            self.fullAudioData = np.append(self.fullAudioData, chunk.rawData)
            MessageServer.notifyEventClients(MsgTypes.UPDATE_PCM_CHART)
            chunkHighestFreq = self.findHighestFreqFromFFT(fftData=chunk.chunkFFT, freqs=chunk.chunkFreqs)
            self.realTimeFrequencyEnvelope.append(chunkHighestFreq)
            print("chunkHighestFreq[{}] = {}".format(len(self.realTimeFrequencyEnvelope), chunkHighestFreq))
    
    # MessageClient
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.NEW_RECORDING: {self.realTimeFrequencyEnvelope.clear(), self.realTimePCMEnvelope.clear()}
        }[msgType]
    
    # ______________________________________________________________________
    
    def getCurrentChunk(self):
        return self.recordChunks[-1]
    
    def getCurrentChunkFreq(self):
        return self.recordChunks[-1].chunkFreqs
    
    def getCurrentChunkFFT(self):
        return self.recordChunks[-1].chunkFFT
    
    def getCurrentRTChunk(self):
        return self.realTimeChunks[-1]
    
    def getCurrentRTChunkFreq(self):
        return self.realTimeChunks[-1].chunkFreqs
    
    def getCurrentRTChunkFFT(self):
        return self.realTimeChunks[-1].chunkFFT
    
    def getChunk(self, nr: int):
        return self.realTimeChunks[nr].rawData
    
    def getChunkFFT(self, nr: int):
        return self.realTimeChunks[nr].chunkFFT
