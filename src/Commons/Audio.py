class Audio:
    filePath: str = None
    data = None
    numberOfFrames: int = None
    numberOfChannels: int = None
    sampleWidth: int = None
    frameRate: int = None
    compType: str = None
    compName: str = None
        
    #getInformationsAsATuple
    @classmethod
    def getInformations(self):
        return self.filePath, self.numberOfChannels, self.sampleWidth, self.frameRate, self.numberOfFrames, self.compType, self.compName
    
    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data

    @classmethod
    def setFields(self,filePath, nchannels, sampwidth, framerate, nframes, comptype, compname):
        """ Sets class variables(just as static fields) to goven values"""
        self.filePath = filePath
        self.numberOfChannels = nchannels
        self.sampleWidth = sampwidth
        self.frameRate = framerate
        self.numberOfFrames = nframes
        self.compType = comptype
        self.compName = compname

    def withFields(self, filePath, nchannels, sampwidth, framerate, nframes, comptype, compname):
        """ Sets class INSTANCE fields to given values and returns object instance"""
        self.filePath = filePath
        self.numberOfChannels = nchannels
        self.sampleWidth = sampwidth
        self.frameRate = framerate
        self.numberOfFrames = nframes
        self.compType = comptype
        self.compName = compname
        return self
