class Audio:
    data = None
    numberOfFrames = None
    numberOfChannels = None
    sampleWidth = None
    frameRate = None
    compType = None
    compName = None

    # getInformationsAsATuple
    @classmethod
    def getInformations(self):
        return self.numberOfChannels, self.sampleWidth, self.frameRate, self.numberOfFrames, self.compType, self.compName
    
    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data

    @classmethod
    def setFields(self, nchannels, sampwidth, framerate, nframes, comptype, compname):
        self.numberOfChannels = nchannels
        self.sampleWidth = sampwidth
        self.frameRate = framerate
        self.numberOfFrames = nframes
        self.compType = comptype
        self.compName = compname
