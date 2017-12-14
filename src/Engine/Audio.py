import numpy as np
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from .Chunk import Chunk
import abc
from collections import deque


class Audio(abc.ABC):
    def __init__(self):
        self.chunks = []  # np.ones(0, dtype=Chunk)
        self.currentLiveProcessedChunkNr = 0
        
        self.minFrequency: int = None
        self.maxFrequency: int = None
        
        self.currentLiveProcessedChunk = None
        self.nfrequencyEnvelopes: [] = []
        self.absolutePCMEnvelope: [] = []

    
    def getCurrentLiveProcessedChunk(self):
        #TODO: !!!
        return self.chunks[self.currentLiveProcessedChunkNr]
    
    def getLastNChunks(self, n: int):
        return self.chunks[:-n]
    
    def getNChunks(self, startIndex: int, stopIndex: int):
        return self.chunks[startIndex:stopIndex]