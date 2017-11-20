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
        self.pyAudio = pyaudio.PyAudio()
        self._staticAudio = staticAudio
        outputDevices = validateOutputDevices(self.pyAudio)
        
        if len(outputDevices) == 0:
            raise Exception("No valid input devices found!")  # TODO: Should this be here or in validOutputDevices?
    
    def open(self):
        self._stream = self.pyAudio.open(format=Cai.sampleWidthPyAudio, channels=Cai.numberOfChannels,
                                         rate=Cai.frameRate, output=True)
        Logger.info("Opening output stream")
    
    def writeChunk(self, data):
        # staticAudioChunk = self._staticAudio.getCurrentLiveProcessedChunk()
        # TODO: mix theses samples and then write.
        self._stream.write(data)
    
    def closeOutputStream(self):
        self._stream.close()
        self.pyAudio.terminate()
        Logger.info("Output stream closed.")
    
    # for observer pattern___________________________________________________
    
    def handleNewData(self, data):
        # self._newStreamThread(data.tostring())
        self.writeChunk(data.tostring())

    def handleMessage(self, msgType, data):
        return {
            MsgTypes.NEW_CURRENT_CHUNK: self.setCurrentProcessedChunkNr,
        }[msgType](data)

    def setCurrentProcessedChunkNr(self, nr: int):
        self.currentProcessedChunkNr = nr