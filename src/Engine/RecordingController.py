from src.MessageServer import MessageServer, MsgTypes
from src.tools.Logger import Logger
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
import wave
import numpy as np
from time import gmtime, strftime

class Recording:
    def __init__(self):
        self.nrOfrecordedFrames = 0
    
    @classmethod
    def startRecording(self):
        Logger.info("Starting recording")
        MessageServer.notifyEventClients(MsgTypes.NEW_RECORDING)
        
    @classmethod
    def stopRecording(self):
        MessageServer.notifyEventClients(MsgTypes.RECORDING_STOP)
        self._shouldRecord = False
        Logger.info("Stopping recording.")
        
    def pauseRecording(self):
        raise NotImplementedError()

    @classmethod
    def saveRecordedDataToFile(self, pcm: np.ndarray, fileName='Record'):
        fileName += strftime("_%Y-%m-%d_%H-%M-%S", gmtime())
        waveFile = wave.open(fileName + ".wav", 'wb')
        waveFile.setnchannels(Cai.numberOfChannels)
        waveFile.setsampwidth(Cai.sampleWidthInBytes)
        waveFile.setframerate(Cai.frameRate)
        waveFile.writeframes(pcm.tostring())
        Logger.info("Saving recorded data as: " + fileName)
        waveFile.close()
