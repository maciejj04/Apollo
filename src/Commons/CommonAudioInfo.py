from pyaudio import paInt16
import numpy as np

class CommonAudioInfo:
    numberOfFrames = None  # defines nr of frames which are going to be recorded(length of input file)
    numberOfChannels = 1
    sampleWidthInBytes = 2
    sampleWidthPyAudio = paInt16
    sampleWidthNumpy = np.int16
    frameRate = None
    compType = None
    compName = None
    
    updatesPerSecond = 10  # TODO: to be externalized as user settings.
    
    # chunk = lambda self: int(self.frameRate/self.updatesPerSecond)
    
    @classmethod
    def getChunk(self):
        return int(self.frameRate / self.updatesPerSecond)
    
    @classmethod
    def getInformations(self):
        return self.numberOfChannels, self.sampleWidthInBytes, self.frameRate, self.numberOfFrames, self.compType, self.compName, self.updatesPerSecond
    
    def setFields(self, nchannels, sampleWidthInBytes, sampleWidthPyAudio, framerate, nframes, comptype, compname):
        self.numberOfChannels = nchannels
        self.sampleWidthInBytes = sampleWidthInBytes
        self.sampleWidthPyAudio = sampleWidthPyAudio
        self.frameRate = framerate
        self.numberOfFrames = nframes
        self.compType = comptype
        self.compName = compname
