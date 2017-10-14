from pyaudio import paInt16


class CommonAudioInfo:
    numberOfFrames = None  # defines nr of frames which are going to be recorded(similar to length of input file)
    numberOfChannels = 1
    sampleWidthInBytes = 2
    sampleWidthPyAudio = paInt16
    frameRate = None
    compType = None
    compName = None
    
    updatesPerSecond = 100  # Should this be moved to InterpretEngine?
    
    # chunk = lambda self: int(self.frameRate/self.updatesPerSecond)
    
    @classmethod
    def getChunk(self):
        return int(self.frameRate / self.updatesPerSecond)
    
    # getInformationsAsATuple
    @classmethod
    def getInformations(self):
        return self.numberOfChannels, self.sampleWidthInBytes, self.frameRate, self.numberOfFrames, self.compType, self.compName
    
    def setFields(self, nchannels, sampwidthInBytes, sampleWidthPyAudio, framerate, nframes, comptype, compname):
        self.numberOfChannels = nchannels
        self.sampleWidthInBytes = sampwidthInBytes
        self.sampleWidthPyAudio = sampleWidthPyAudio
        self.frameRate = framerate
        self.numberOfFrames = nframes
        self.compType = comptype
        self.compName = compname
