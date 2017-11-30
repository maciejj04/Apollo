from datetime import datetime

#from src.Commons.Audio import Audio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


class Logger:
    # static method - code that belongs to a class, but that doesn't use the object itself at all.
    @staticmethod
    def info(infoString: str):
        print('[' + str(datetime.now()) + '] ' + infoString)
        # TODO: add writing to file
    
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
                         - updatesPerSecond {}\n""" \
            .format(Cai.getChunkSize(), Cai.frameRate, Cai.numberOfChannels, Cai.sampleWidthInBytes, Cai.compType,
                    Cai.compName, Cai.updatesPerSecond, dateTime=str(datetime.now()))
        print(infoString)
        # TODO: save string to file.

    @staticmethod
    def interpretEngineLog(string: str):
        prefix = " InterpretEngine Log: "
        print(prefix + string)
        Logger._writeLogToFile(string, prefix=prefix)
        
        
    @staticmethod
    def _writeLogToFile(string: str, prefix: str=""):
        from configuration import LOGS_DIR
        import os
        with open(os.path.join(LOGS_DIR, "interpretLog.txt"), "a") as text_file:
            text_file.write(prefix + "; " + string)