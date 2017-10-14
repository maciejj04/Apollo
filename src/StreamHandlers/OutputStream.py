import pyaudio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
class OutputStream:
    
    stream = None
    pyAudio = None
    
    def __init__(self):
        self.pyAudio = pyaudio.PyAudio()
        self.stream = self.pyAudio.open(
                format=Cai.sampleWidthPyAudio,
                channels=Cai.numberOfChannels,
                rate=Cai.frameRate,
                output=True
        )
    
    def playChunk(self, data):
        #while data != '':
        self.stream.write(data)

    def closeOutputStream(self):
        self.stream.close()
        self.pyAudio.terminate()