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


class ProcessingEngine(BaseProcessingUtils, Observer, MessageClient, Observable):
    currentChunkNr: int = -1
    
    def __init__(self, staticAudio: StaticAudio):
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
    def findLoudestFreqFromFFT(SAData: np.ndarray, freqs=None) -> int:
        if freqs is None:
            freqs = np.fft.fftfreq(len(SAData))
        
        idx = np.argmax(np.abs(SAData))  # TODO: FFT from chunk is already absolute!
        freq = freqs[idx]
        freq_in_hertz = abs(freq)  # * Cai.frameRate)
        return freq_in_hertz
    
    @staticmethod
    def findNLoudestFreqsFromFFT(spectrum: np.ndarray, freqs) -> np.ndarray:
        from src.Commons.Settings import TOP_FREQS_COUNT
        maxValuesIndexes = np.argsort(spectrum)[-TOP_FREQS_COUNT:]
        freqsInHertz = np.array([], dtype=np.float64)
        
        for i in np.nditer(maxValuesIndexes):
            freqsInHertz = np.append(freqsInHertz, abs(freqs[i]))  # * Cai.frameRate)
        return freqsInHertz
    
    @staticmethod
    def calculateSpectralCentroid(AmpSpectr: np.ndarray, freqs: np.ndarray):
        """
        Calculates spectral centroid as pointed in https://en.wikipedia.org/wiki/Spectral_centroid
        and
        https://dsp.stackexchange.com/questions/27499/finding-the-right-measure-to-compare-sound-signals-in-the-frequency-domain/27533#27533
        """
        maxValIndex = np.max(AmpSpectr)
        normalizedAmpSpecrt = AmpSpectr / maxValIndex  # delete it :'D
        
        sum = 0
        discriminator = 0
        for i in range(0, len(normalizedAmpSpecrt)):
            sum += normalizedAmpSpecrt[i] * freqs[i]
            discriminator += normalizedAmpSpecrt[i]
        
        return sum / discriminator
        
    def getCurrentLiveAudio(self) -> LiveAudio:
        return self.liveAudios[-1]
    
    def _calculateStaticAudioParameters(self):
        def calculateNMaxFreqsEnvelopes():
            from src.Commons.Settings import TOP_FREQS_COUNT
            envelopes = []
            for i in range(0, TOP_FREQS_COUNT):
                envelopes.append([])
                
            for c in self.staticAudio.chunks:
                freqs = ProcessingEngine.findNLoudestFreqsFromFFT(c.chunkAS, c.chunkFreqs)
                freqs = np.sort(freqs)
                for i in range(0, freqs.size):
                    envelopes[i].append(freqs[i])
            return envelopes
            
        #self.calculateFrequencyEnvelopeForAudio(self.staticAudio)
        envelopes = calculateNMaxFreqsEnvelopes()
        self.staticAudio.frequencyEnvelope = envelopes
    
    def processChunkAndAppendToLiveData(self, chunk: Chunk):
        # TODO: should load plugin analysis
        loudestFreqInHertz = ProcessingEngine.findLoudestFreqFromFFT(SAData=chunk.chunkAS, freqs=chunk.chunkFreqs)
        nLoudestFreqsInHertz = ProcessingEngine.findNLoudestFreqsFromFFT(spectrum=chunk.chunkAS, freqs=chunk.chunkFreqs)
        nLoudestFreqsInHertz = np.sort(nLoudestFreqsInHertz).tolist()
        currentLiveAudio = self.getCurrentLiveAudio()
        currentLiveAudio.parameters["frequencyEnvelope"].append(loudestFreqInHertz)
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQS_CHART, data={"liveFreqsEnvelope": nLoudestFreqsInHertz})
        self.notifyObservers(currentLiveAudio)
        # currentLiveAudio.parameters["PCMEnvelope"].append()
    
    def setupNewLiveRecording(self):
        self.liveAudios.append(LiveAudio())

    
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
    # __________________________________________________________________________________________

    # Used by observer pattern!
    def handleNewData(self, data):
        self.currentChunkNr += 1
        chunk = Chunk(data, self.currentChunkNr)
        self.currentLiveChunk = chunk
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQ_SPECTR_CHART, chunk)

        if self.shouldSave:
            self.getCurrentLiveAudio().appendNewChunkAndRawData(chunk)
            self.processChunkAndAppendToLiveData(chunk)

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
    
    def notifyObservers(self, data):
        for o in self.getObservers:
            o.handleNewData(data)
