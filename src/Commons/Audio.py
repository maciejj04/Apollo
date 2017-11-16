from pydub import AudioSegment
from src.Engine.Converter import Converter
import wave, os, sys
import numpy as np
from src.tools.Logger import Logger
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from datetime import datetime


class Audio:
    filePath: str
    data = None
    numberOfFrames: int = None
    numberOfChannels: int = None
    sampleWidth: int = None
    frameRate: int = None
    compType: str = None
    compName: str = None
    
    def __init__(self, filePath='./resources/g1.wav'):#saxophone-weep, 220_440
        self.filePath = filePath

    def loadFromPathAndAdjust(self, filePath: str = None):
        
        if filePath is None or filePath == "":
            filePath = self._getInputArguments()
        
        Audio.filePath = filePath
        self._validateFilePath(filePath)
        
        self.wav = Converter.adjustAudioFormat(self._getAnyAsWave())
        Audio.setFields(filePath, self.wav.getnchannels(), self.wav.getsampwidth(), self.wav.getframerate(),
                        self.wav.getnframes(), self.wav.getcompname(), self.wav.getcompname())
        Cai.numberOfFrames = self.wav.getnframes()
        
        self._logAudioInfo()
        return self
    
    def getRawDataFromWav(self, wav=None):
        if wav is None:
            wav = self.wav.getnframes()
        frames = self.wav.readframes(wav)
        self.wav.close()
        return np.fromstring(frames, dtype=np.int16)
    
    def _validateFilePath(self, filePath):
        if not os.path.exists(filePath):
            Logger.info("Path to file does not exist! [{filepath}]".format(filepath=filePath))
            raise ValueError("Path to file does not exist! [{filepath}]".format(filepath=filePath))
        
        return True
    
    def _getInputArguments(self):
        return self.filePath if len(sys.argv) < 2 else sys.argv[1]

    def _getAnyAsWave(self, exportPath='./tmp/basicConvertedToWavResourceAudio.wav'):
        """
        :param filePath:
        :param exportPath:
        :return: Wave_read object
        Fction should take any (TODO) audio file format hidden undaer filePath, convert it into wave and return with wave.open().
        """
        fileToConvert = AudioSegment.from_file(self.filePath)
        # TODO: why pydub automatically converts 4byte width frame to 2byte while converting from mp3 to wav
        fileToConvert.export(out_f=exportPath, format="wav")
        return wave.open(exportPath, 'r')

    # getInformationsAsATuple
    
    @classmethod
    def getInformations(self):
        return self.filePath, self.numberOfChannels, self.sampleWidth, self.frameRate, self.numberOfFrames, self.compType, self.compName
    
    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data
    
    @classmethod
    def setFields(self, filePath, nchannels, sampwidth, framerate, nframes, comptype, compname):
        """ Sets class variables(just as static fields) to gi ven values"""
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
    
    def _logAudioInfo(self):
        
        Logger.info('''[{dateTime}] You choose : {}\t
                         - nrOfFrames: {}
                         - framerate: {}
                         - nchannels: {}
                         - sampwidth {} (in bytes)
                         - comptype {}
                         - compname {}
                 - these are converted audio file informations'''#audio data will be converted to input device audio format - to properly operate on this two files
                    .format(self.filePath, self.numberOfFrames, self.frameRate, self.numberOfChannels, self.sampleWidth,
                            self.compType, self.compName,
                            dateTime=str(datetime.now()))
                    )
    
    class OrgAudioInfo:
        pass
