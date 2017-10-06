class CommonAudioInfo:
    numberOfFrames = None
    numberOfChannels = 1
    sampleWidth = None
    frameRate = None
    compType = None
    compName = None
    
    updatesPerSecond = 10   #SHould this be moved to InterpretEngine?
    #chunk = lambda self: int(self.frameRate/self.updatesPerSecond)

    @classmethod
    def getChunk(self):
        return int(self.frameRate/self.updatesPerSecond)
    
    # getInformationsAsATuple
    @classmethod
    def getInformations(self):
        return self.numberOfChannels, self.sampleWidth, self.frameRate, self.numberOfFrames, self.compType, self.compName

    def setFields(self, nchannels, sampwidth, framerate, nframes, comptype, compname):
        self.numberOfChannels = nchannels
        self.sampleWidth = sampwidth
        self.frameRate = framerate
        self.numberOfFrames = nframes
        self.compType = comptype
        self.compName = compname
