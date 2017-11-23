import numpy as np
from src.Engine.Chunk import Chunk
from .ProcessingEngine import ProcessingEngine
from src.tools.Logger import Logger

# class is a observer. Observes if new data comes in!
class InterpretEngine:
    
    def __init__(self):
        pass
    
    def handleNewData(self):
        pass
    
    def getFFTsCorrelation(self, staticChunk: Chunk, liveChunk: Chunk):
        pass
    
    def measurePCMsCrossCorelation(self, staticChunk: Chunk, liveChunk: Chunk):
        crossCorr = np.coorelate(staticChunk.rawData, liveChunk.rawData)
        print(crossCorr)