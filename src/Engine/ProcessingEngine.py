from src.Engine.PluginModule.PluginHandler import PluginHandler
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
        self.pluginsHandler: PluginHandler = PluginHandler()
    
    def calculateFrequencyEnvelopeForAudio(self, audio: Audio):
        for c in audio.chunks:
            freq = ProcessingEngine.findLoudestFreqFromFFT(c.chunkAS, c.chunkFreqs)
            audio.nfrequencyEnvelopes.append(freq)
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
    def calculateSpectralCentroid(ampSpectr: np.ndarray, freqs: np.ndarray):
        """
        Calculates spectral centroid as pointed in https://en.wikipedia.org/wiki/Spectral_centroid
        and
        https://dsp.stackexchange.com/questions/27499/finding-the-right-measure-to-compare-sound-signals-in-the-frequency-domain/27533#27533
        """
        maxValIndex = np.max(ampSpectr)
        normalizedAmpSpecrt = ampSpectr / maxValIndex  # delete it :'D
        
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
                freqs = np.sort(
                            ProcessingEngine.findNLoudestFreqsFromFFT(c.chunkAS, c.chunkFreqs))
                
                for i in range(0, freqs.size):
                    envelopes[i].append(freqs[i])
            return envelopes
        
        # self.calculateFrequencyEnvelopeForAudio(self.staticAudio)
        self.staticAudio.absolutePCMEnvelope = ProcessingEngine.calculateAbsolutePCMEnvelope(self.staticAudio.rawData)
        envelopes = calculateNMaxFreqsEnvelopes()
        self.staticAudio.nfrequencyEnvelopes = envelopes
        for ch in self.staticAudio.chunks:
            ch.baseFrequency = ProcessingEngine.estimateHzByAutocorrelationMethod(ch.rawData)
            Logger.info("Cunks[{nr}] base Hz = {fq}".format(nr=ch.chunkNr, fq=ch.baseFrequency))
    
    @staticmethod
    def estimateHzByAutocorrelationMethod(signal: np.ndarray):
        from scipy.signal import fftconvolve
        from numpy import diff, argmax
        from matplotlib.mlab import find
        """Estimate frequency using autocorrelation

        Pros: Best method for finding the true fundamental of any repeating wave,
        even with strong harmonics or completely missing fundamental

        """
        
        fs = Cai.frameRate
        
        def parabolic(f, x):
            xv = 1 / 2 * (f[x - 1] - f[x + 1]) / (f[x - 1] - 2 * f[x] + f[x + 1]) + x
            yv = f[x] - 1 / 4 * (f[x - 1] - f[x + 1]) * (xv - x)
            return xv, yv
        
        # Calculate circular autocorrelation (same thing as convolution, but with
        # one input reversed in time), and throw away the negative lags
        corr = fftconvolve(signal, signal[::-1], mode='full')
        corr = corr[int(len(corr) / 2):]
        
        # Find the first low point
        d = diff(corr)
        start = find(d > 0)[0]  # TODO: bug! Crashes when array consists of zeros
        
        # Find the next peak after the low point (other than 0 lag).  This bit is
        # not reliable for long signals, due to the desired peak occurring between
        # samples, and other peaks appearing higher.
        # Should use a weighting function to de-emphasize the peaks at longer lags.
        # Also could zero-pad before doing circular autocorrelation.
        peak = argmax(corr[start:]) + start  # TODO: replace argmax
        px, py = parabolic(corr, peak)
        
        return fs / px
    
    @staticmethod
    def calculateAbsolutePCMEnvelope(signal: np.ndarray):  # obwiednia
        
        envelope = ProcessingEngine\
            .lowPassFilter(
                np.array(
                    [abs(x) for x in signal]
                ), n=18
        )
        return envelope
    
    @staticmethod
    def lowPassFilter(signal: np.ndarray, n=3):
        new = []
        for i in range(0, signal.size - int(n / 2), 1):
            new.append(np.mean(signal[i:i + n]))
    
        return new


    def processLastChunk(self):

        currentLiveAudio = self.getCurrentLiveAudio()
        chunk = currentLiveAudio.getLastChunk()
        loudestFreqInHertz = ProcessingEngine.findLoudestFreqFromFFT(SAData=chunk.chunkAS, freqs=chunk.chunkFreqs)
        nLoudestFreqsInHertz = ProcessingEngine.findNLoudestFreqsFromFFT(spectrum=chunk.chunkAS, freqs=chunk.chunkFreqs)
        nLoudestFreqsInHertz = np.sort(nLoudestFreqsInHertz).tolist()
        currentLiveAudio.appendFreqEnvelopesValues(*nLoudestFreqsInHertz)
        
        currentLiveAudio.getLastChunk().baseFrequency = ProcessingEngine.estimateHzByAutocorrelationMethod(
            chunk.rawData)
        
        currentLiveAudio.parameters["frequencyEnvelope"].append(loudestFreqInHertz)
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQS_CHART, data={"liveFreqsEnvelope": nLoudestFreqsInHertz})
        self.notifyObservers(currentLiveAudio)
        # currentLiveAudio.parameters["PCMEnvelope"].append()
    
    def setupNewLiveRecording(self):
        self.liveAudios.append(LiveAudio())
    
    def signalMatching(self, staticAudioRawData: np.ndarray, liveAudioRawData: np.ndarray):
        pass
        
        
        
    #__________________________________________________________________________________________
    
    # Used by observer pattern!
    def handleNewData(self, data):
        self.currentChunkNr += 1
        chunk = Chunk(data, self.currentChunkNr)
        self.currentLiveChunk = chunk
        MessageServer.notifyEventClients(MsgTypes.UPDATE_FREQ_SPECTR_CHART, chunk)
        ProcessingEngine.calculateAbsolutePCMEnvelope(chunk.rawData)
        
        if self.shouldSave:
            self.pluginsHandler.handleNewChunk(chunk.rawData)
            self.getCurrentLiveAudio().appendNewChunkAndRawData(chunk)
            self.processLastChunk()
    
    # MessageClient___________________________________________________________________________----
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
            
