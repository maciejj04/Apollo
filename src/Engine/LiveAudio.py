from .Audio import Audio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
import numpy as np
from src.MessageServer import MessageServer, MsgTypes
from src.MessageClient import MessageClient
from src.Engine.Chunk import Chunk
from src.Engine.RecordingController import Recording

class LiveAudio(Audio):
    def __init__(self):
        Audio.__init__(self)
        #MessageServer.registerForEvent(self, MsgTypes.NEW_CURRENT_CHUNK)
        
        self.fullRawAudioData = np.ones(0, dtype=Cai.sampleWidthNumpy)
        
        self.frequencyEnvelope = []
        self.PCMEnvelope = []
        
        self.parameters = {
            "frequencyEnvelope": [],
            "PCMEnvelope": []
        }
        
        self.maxNrOfChunks = Cai.numberOfFrames/Cai.getChunkSize()
    
    # def handleMessage(self, msgType, data):
    #     return {
    #         MsgTypes.NEW_CURRENT_CHUNK: self._setCurrentProcessedChunkNr(data)
    #     }[msgType]

    def appendNewChunkAndRawData(self, chunk: Chunk):
        if len(self.chunks) >= self.maxNrOfChunks:
            Recording.stopRecording()
            Recording.saveRecordedDataToFile(self.fullRawAudioData)
            return
        self.chunks.append(chunk)
        np.append(self.fullRawAudioData, chunk.rawData)  # TODO: check whether it works fine

    def _setCurrentProcessedChunkNr(self, nr):
        self.currentLiveProcessedChunkNr = nr
