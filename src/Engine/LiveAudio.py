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
        
        self.PCMEnvelope = []
        
        self.parameters = {
            "frequencyEnvelope": [],
            "PCMEnvelope": []
        }
        
        self.maxNrOfChunks = int(Cai.numberOfFrames/Cai.getChunkSize())
    
    # def handleMessage(self, msgType, data):
    #     return {
    #         MsgTypes.NEW_CURRENT_CHUNK: self._setCurrentProcessedChunkNr(data)
    #     }[msgType]

    def appendNewChunkAndRawData(self, chunk: Chunk):
        self.chunks.append(chunk)
        self.fullRawAudioData = np.append(self.fullRawAudioData, chunk.rawData)  # TODO: check whether it works fine

        if len(self.chunks) >= self.maxNrOfChunks:
            Recording.stopRecording()
            Recording.saveRecordedDataToFile(self.fullRawAudioData)

    def _setCurrentProcessedChunkNr(self, nr):
        self.currentLiveProcessedChunkNr = nr
    
    def getLastChunk(self):
        return self.chunks[len(self.chunks)-1]

    def getLastChunksIndex(self):
        return len(self.chunks)
    
    def getFrequencyEnvelope(self) -> []:
        return self.parameters["frequencyEnvelope"]