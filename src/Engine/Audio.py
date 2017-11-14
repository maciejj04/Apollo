import numpy as np
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from .Chunk import Chunk
import abc

class Audio(abc.ABC):
    def __init__(self):
        
        self.chunks = []  # np.ones(0, dtype=Chunk)
        self.currentLiveProcessedChunkNr = 0
        
        self.minFrequency = None
        self.maxFrequency = None
        
        
    def getLastNChunks(self, n: int):
        return self.chunks[:-n]
        
    def getFullAudioRawData(self):
        pass
    
    def getCurrentLiveProcessedChunk(self):
        return self.chunks.item(self.currentLiveProcessedChunkNr)