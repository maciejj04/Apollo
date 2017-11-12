import pyaudio
import pyaudio
from src.StreamHandlers.Stream import Stream
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.StreamHandlers.ValidateOutputDevices import validateOutputDevices
from src.Observer import Observer

DEFAULT_DEVICE_INDEX = 0


class OutputStreamHandler(Observer):
    # TODO: needs to be informed about new data that comes both from mic(done) and corresponding inputaudio file chunk ;'D
    
    def __init__(self):
        self.pyAudio = pyaudio.PyAudio()
        outputDevices = validateOutputDevices(self.pyAudio)
        
        if len(outputDevices) == 0:
            raise Exception("No valid input devices found!")  # TODO: Should this be here or in validOutputDevices?
        
    
    def open(self):
        self._stream = self.pyAudio.open(format=Cai.sampleWidthPyAudio, channels=Cai.numberOfChannels,
                                            rate=Cai.frameRate, output=True)
    
    def writeChunk(self, data):
        # while data != '':
        self._stream.write(data)
    
    def closeOutputStream(self):
        self._stream.close()
        self.pyAudio.terminate()
    
    #for observer pattern___________________________________________________
    def handleNewData(self, data, shouldSave=False):
        self.writeChunk(data.tostring())