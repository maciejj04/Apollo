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
from src.Engine.Audio import Audio
from src.tools.Logger import Logger

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
    
    def calculateFrequencyEnvelopeForAudio(self, audio: Audio):
        for c in audio.chunks:
            freq = ProcessingEngine.findLoudestFreqFromFFT(c.chunkAS, c.chunkFreqs)
            audio.frequencyEnvelope.append(freq)
            Logger.info("{0}. ChunksFreq = {1}".format(c.chunkNr, freq))
            
    @staticmethod
    def findHighestFreqFromRawData(data: np.ndarray) -> int:
        """
        :return: highestFrequency in hertz
        """
        freq, fft = BaseProcessingUtils.getAplitudeSpectrum(data, Cai.frameRate)
        return ProcessingEngine.findLoudestFreqFromFFT(fft, freq)
    
    @staticmethod
    def findLoudestFreqFromFFT(SAData: np.ndarray, freqs=None) -> int:
        if freqs is None:
            freqs = np.fft.fftfreq(len(SAData))
        
        idx = np.argmax(np.abs(SAData))  # TODO: FFT from chunk is already absolute!
        freq = freqs[idx]
        freq_in_hertz = abs(freq)  # * Cai.frameRate)
        return freq_in_hertz

    # @staticmethod
    # def findNLoudestFreqsFromFFT(spectrum: np.ndarray, freqs, n) -> int:
    #
    #     values = np.argsort(spectrum)[-n]
    #     freqsInHertz = np.array([], dtype=np.int16)
    #
    #     for v in values.tolist():
    #         freqsInHertz = np.append(freqsInHertz, abs(v))  # * Cai.frameRate)
    #     return freqsInHertz



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
        return self.recordChunks[-1].chunkAS
    
    def getCurrentRTChunk(self):
        return self.realTimeChunks[-1]
    
    def getCurrentRTChunkFreq(self):
        return self.getCurrentLiveAudio().chunks[-1].chunkFreq
    
    def getCurrentRTChunkFFT(self):
        return self.getCurrentLiveAudio().chunks[-1].chunkAS

    def getChunksRawData(self, nr: int):
        return self.getCurrentLiveAudio().chunks[nr].rawData
    
    def getChunkFFT(self, nr: int):
        return self.getCurrentLiveAudio().chunks[nr].chunkAS

    def getCurrentChunksFrequencySpectrum(self):
        return self.currentLiveChunk.chunkAS

    def setupNewLiveRecording(self):
        self.liveAudios.append(LiveAudio())

    def _calculateStaticAudioParameters(self):
        # clacualte from pulgins
        self.calculateFrequencyEnvelopeForAudio(self.staticAudio)
        
        
    def processChunkAndAppendToLiveData(self, chunk: Chunk):
        # TODO: should load plugin analysis
        freqInHertz = ProcessingEngine.findLoudestFreqFromFFT(SAData=chunk.chunkAS, freqs=chunk.chunkFreqs)

        # nLoudest = ProcessingEngine.findNLoudestFreqsFromFFT(spectrum=chunk.chunkAS, freqs=chunk.chunkFreqs, n=3)
        # print("N Loudest freqs")
        # for i in nLoudest.tolist():
        #     print("%d, " %i)
        
        currentLiveAudio = self.getCurrentLiveAudio()
        currentLiveAudio.parameters["frequencyEnvelope"].append(freqInHertz)
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQS_CHART, data={"liveFreqsEnvelope": freqInHertz})
        self.notifyObservers(currentLiveAudio)
        #currentLiveAudio.parameters["PCMEnvelope"].append()
        
    # !! Only Offline for now!
    # def signalMatching(self, staticAudioRawData: np.ndarray, liveAudioRawData: np.ndarray):
    #
    #     windowWidth = Cai.getChunkSize()  # depends on computer resources. For now it's 4410/10=441
    #     step = Cai.getChunkSize()/10 # depends on computer resources. For now it's 4410/10=441
    #     # Takes
    #     for index in range(0, staticAudioRawData.size)
    #
    #     #Iterates over rawData by windowWidth and calculates coorelation.
    #     for elementNr in range(0, staticAudioRawData.size, windowWidth):
        
        
        
        
    def notifyObservers(self, data):
        for o in self.getObservers:
            o.handleNewData(data)
