from datetime import datetime

from src.Commons.Audio import Audio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


class Logger:
    #static method - code that belongs to a class, but that doesn't use the object itself at all.
    @staticmethod
    def info(infoString: str):
        print('['+str(datetime.now())+'] '+infoString)
        #TODO: add writing to file
    
        
    def saveToLogFile(self):
        pass
    
    
    @staticmethod
    def logCommonAudioInformations():
        infoString = """[{dateTime}] Common Audio data parameters were set at:
                         - nrOfFramesPerBuffer(chunk): {}
                         - framerate: {}
                         - nchannels: {}
                         - sampwidth {} (in bytes)
                         - comptype {}
                         - compname {}
                         - updatesPerSecond {}"""\
            .format(Cai.getChunk(), Cai.frameRate, Cai.numberOfChannels, Cai.sampleWidthInBytes, Cai.compType,
                    Cai.compName, Cai.updatesPerSecond,dateTime=str(datetime.now()))
        print(infoString)
        # TODO: save string to file.
    
    
    @staticmethod
    def logAudioInfo(audio: Audio=None):
        
        if audio is None:
            audio = Audio()#get static fields when nothing passed
            
        (filePath, nchannels, sampwidth, framerate, nframes, comptype, compname) = audio.getInformations()
    
        print('''[{dateTime}] You choose : {}\t
                         - nrOfFrames: {}
                         - framerate: {}
                         - nchannels: {}
                         - sampwidth {} (in bytes)
                         - comptype {}
                         - compname {}
                 - these are original audio file informations, audio data will be converted to input device audio format - to properly operate on this two files'''
              .format(filePath, nframes, framerate, nchannels, sampwidth, comptype, compname, dateTime=str(datetime.now())))
        
        # TODO: save to log file
