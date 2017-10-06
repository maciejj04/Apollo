from Audio import Audio

class Logger:
    #static method - code that belongs to a class, but that doesn't use the object itself at all.
    @staticmethod
    def info():
        pass;
    
    @staticmethod
    def logAudioInfo(filePath):
        
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = Audio.getInformations()
    
        print('''You choose : {}\t
                         - nrOfFrames: {}
                         - framerate: {}
                         - nchannels: {}
                         - sampwidth {} (in bytes)
                         - comptype {}
                         - compname {}'''
              .format(filePath, nframes, framerate, nchannels, sampwidth, comptype, compname))
        
        # TODO: save to log file
