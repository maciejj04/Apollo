import numpy as np
from .Audio import Audio
from src.MessageClient import MessageClient
from src.MessageServer import MessageServer, MsgTypes
from src.Engine.Chunk import Chunk
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


class StaticAudio(Audio, MessageClient):
    def __init__(self, rawData: np.ndarray):
        MessageServer.registerForEvent(self, MsgTypes.NEW_CURRENT_CHUNK)

        self.calculateChunks(rawData)
        
        self.currentLiveProcessedChunk = None
    
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.NEW_CURRENT_CHUNK: self._setCurrentProcessedChunkNr(data)
        }[msgType]
    
    def _setCurrentProcessedChunkNr(self, nr: int):
        self.currentLiveProcessedChunk = nr

    def getCurrentLiveProcessedChunk(self):
        return self.chunks.item(self.currentLiveProcessedChunkNr)
    
    
    
    
    
    
    def calculateChunks(self, rawData):
        chunkSize = Cai.getChunkSize()
        i=0
        for chunkByte in range(0, rawData.size - Cai.numberOfFrames, Cai.numberOfFrames):
            self.chunks.append(Chunk(rawData[chunkByte:chunkByte + chunkSize], i))  #
            i+=1