import threading
import pyaudio
from src.StreamHandlers.Stream import Stream
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.StreamHandlers.ValidateOutputDevices import validateOutputDevices
from src.Observer import Observer
from src.tools.Logger import Logger
from src.MessageServer import MessageServer, MsgTypes
from src.MessageClient import MessageClient
from src.Engine.StaticAudio import StaticAudio

DEFAULT_DEVICE_INDEX = 0


class OutputStream(Observer, MessageClient):
    
    # TODO: needs to be informed about new data that comes both from mic(done) and corresponding inputaudio file chunk ;'D
    
    def __init__(self, staticAudio: StaticAudio):
        MessageServer.registerForEvent(self, MsgTypes.NEW_CURRENT_CHUNK)
        MessageServer.registerForEvent(self, MsgTypes.RECORDING_STOP)
        MessageServer.registerForEvent(self, MsgTypes.NEW_RECORDING)
        self.pyAudio = pyaudio.PyAudio()
        self._staticAudio = staticAudio
        self.isRecording = False
        outputDevices = validateOutputDevices(self.pyAudio)
        
        if len(outputDevices) == 0:
            raise Exception("No valid input devices found!")  # TODO: Should this be here or in validOutputDevices?
    
        self.currentChunkNr = 0
    
    def open(self):
        self._stream = self.pyAudio.open(format=Cai.sampleWidthPyAudio, channels=Cai.numberOfChannels,
                                         rate=Cai.frameRate, output=True)
        Logger.info("Opening output stream")
    
    def writeChunk(self, liveChunk):
        # if not self.isRecording:
        # self._stream.write(liveChunk.tostring())
        #return
        
        #staticAudioChunkRawData = self._staticAudio.getChunk(nr=self.currentChunkNr).rawData
        # signalToWrite = ((staticAudioChunkRawData/2 + liveChunk/2)*0.1).tostring()
        #self._stream.write(signalToWrite)
        #self.currentChunkNr += 1


        # play only input audio when recording
        if self.isRecording:
            staticAudioChunkRawData = self._staticAudio.chunks[self.currentChunkNr].rawData
            self._stream.write(staticAudioChunkRawData.tostring())
            self.currentChunkNr += 1

    def closeOutputStream(self):
        self._stream.close()
        self.pyAudio.terminate()
        self.currentChunkNr = 0
        Logger.info("Output stream closed.")
    
    # for observer pattern___________________________________________________
    
    def handleNewData(self, data):
        # self._newStreamThread(data.tostring())
        self.writeChunk(data)

    def handleMessage(self, msgType, data):
        if msgType == MsgTypes.NEW_CURRENT_CHUNK:
            self.setCurrentProcessedChunkNr(data)
            
        elif msgType == MsgTypes.RECORDING_STOP:
            self._recordingStopped()
        
        elif msgType == MsgTypes.NEW_RECORDING:
            self._newRecording()
            
    def _recordingStopped(self):
        self.isRecording = False
        self.currentChunkNr = 0
        
    def setCurrentProcessedChunkNr(self, nr: int):
        self.currentProcessedChunkNr = nr

    def _newRecording(self):
        self.isRecording = True