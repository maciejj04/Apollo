import numpy as np
from .Audio import Audio
from src.MessageClient import MessageClient
from src.MessageServer import MessageServer, MsgTypes
from src.Engine.Chunk import Chunk
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


# Should be singleton?
class StaticAudio(Audio, MessageClient):
    def __init__(self, rawData: np.ndarray):
        Audio.__init__(self)
        self.rawData = rawData
        self.calculateChunks(rawData)
    
    def _setCurrentProcessedChunkNr(self, nr: int):
        self.currentLiveProcessedChunk = nr
    
    def calculateChunks(self, rawData):
        chunkSize = Cai.getChunkSize()
        i = 0
        for chunkByte in range(0, rawData.size - chunkSize + 1, chunkSize):
            self.chunks.append(Chunk(rawData[chunkByte:chunkByte + chunkSize], i))  #
            i += 1
        
        if rawData.size % Cai.getChunkSize() != 0:
            self.chunks.append(Chunk(rawData[i * chunkSize:], i))
    
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.NEW_CURRENT_CHUNK: self._setCurrentProcessedChunkNr(data)
        }[msgType]
