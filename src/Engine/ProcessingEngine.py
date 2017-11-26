from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.tools.helper_functions import my_range
from typing import Tuple
from src.Observer import Observer
from src.Observable import Observable
import numpy as np
from src.Engine.Chunk import Chunk
from collections import deque
from src.MessageClient import MessageClient
from src.MessageServer import MessageServer, MsgTypes
from src.Engine.StaticAudio import StaticAudio
from src.Engine.LiveAudio import LiveAudio

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

class ProcessingEngine(BaseProcessingUtils, Observer, MessageClient, Observable):
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
    
    def __init__(self, staticAudio: StaticAudio):
        """
        :param data: data in np.array return format form
        """
        Observer.__init__(self)
        Observable.__init__(self)
        MessageServer.registerForEvent(self, MsgTypes.NEW_RECORDING)
        MessageServer.registerForEvent(self, MsgTypes.RECORDING_STOP)

        self.shouldSave = False


        self.staticAudio = staticAudio
        self._calculateStaticAudioParameters()
        self.liveAudios = []
        self.currentLiveChunk: Chunk
        
        
        self.realTimeChunks = deque(maxlen=Cai.numberOfFrames)
        self.realTimeFrequencyEnvelope = deque(maxlen=Cai.numberOfFrames)
        self.realTimePCMEnvelope = deque(maxlen=Cai.numberOfFrames)
    
    def getFrequencyEnvelope(self):
        return self.calculateFrequencyEnvelope() if self.frequencyEnvelope is None else self.frequencyEnvelope
    
    def calculateFrequencyEnvelope(self, rawDataArray=None) -> []:
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
    
    def handleNewData(self, data):
        self.currentChunkNr += 1
        chunk = Chunk(data, self.currentChunkNr)
        self.currentLiveChunk = chunk
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQ_SPECTR_CHART, chunk)
        
        if self.shouldSave:
            self.getCurrentLiveAudio().appendNewChunkAndRawData(chunk)
            self.processChunkAndAppendToLiveData(chunk)
            #print("chunkHighestFreq[{}] = {}".format(len(self.realTimeFrequencyEnvelope), chunkHighestFreq))
    
    # MessageClient
    def handleMessage(self, msgType, data):

        if msgType == MsgTypes.NEW_RECORDING:
            self.setupNewLiveRecording()
            self.shouldSave = True
            return
        elif msgType == MsgTypes.RECORDING_PAUSE:
            raise NotImplementedError()
        elif msgType == MsgTypes.RECORDING_STOP:
            self.shouldSave = False
        else:
            raise Exception("Wrong msgType!! Check impl of MessageService for errors!")
        
    # ______________________________________________________________________
    
    def getCurrentLiveAudio(self) -> LiveAudio:
        return self.liveAudios[-1]
    
    def getCurrentChunk(self):
        return self.getCurrentLiveAudio().getCurrentLiveProcessedChunk()
    
    def getCurrentChunkFreq(self):
        return self.recordChunks[-1].chunkFreqs
    
    def getCurrentChunkFFT(self):
        return self.recordChunks[-1].chunkFFT
    
    def getCurrentRTChunk(self):
        return self.realTimeChunks[-1]
    
    def getCurrentRTChunkFreq(self):
        return self.getCurrentLiveAudio().chunks[-1].chunkFreq
    
    def getCurrentRTChunkFFT(self):
        return self.getCurrentLiveAudio().chunks[-1].chunkFFT

    def getChunksRawData(self, nr: int):
        return self.getCurrentLiveAudio().chunks[nr].rawData
    
    def getChunkFFT(self, nr: int):
        return self.getCurrentLiveAudio().chunks[nr].chunkFFT

    def getCurrentChunksFrequencySpectrum(self):
        return self.currentLiveChunk.chunkFFT

    def setupNewLiveRecording(self):
        self.liveAudios.append(LiveAudio())

    def _calculateStaticAudioParameters(self):
        # clacualte from pulginsA
        self.staticAudioFrequencyEnvelope = self.calculateFrequencyEnvelope(self.staticAudio.rawData)
        
        
    def processChunkAndAppendToLiveData(self, chunk: Chunk):
        # TODO: should load plugin analysis
        freqInHertz = ProcessingEngine.findHighestFreqFromFFT(fftData=chunk.chunkFFT, freqs=chunk.chunkFreqs)
        currentLiveAudio = self.getCurrentLiveAudio()
        currentLiveAudio.parameters["frequencyEnvelope"].append(freqInHertz)
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQS_CHART, data={"liveFreqsEnvelope": freqInHertz})
        self.notifyObservers(currentLiveAudio)
        #currentLiveAudio.parameters["PCMEnvelope"].append()
        
        
    def notifyObservers(self, data):
        for o in self.getObservers:
            o.handleNewData(data)
