import numpy as np
from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from typing import Tuple

class Chunk:
    chunksMinFreq: int
    chunksMaxFreq: int
    
    chunkFFT: np.ndarray
    chunkFreqs: np.ndarray
    
    rawData: np.ndarray = None
    chunkNr: int
    
    def __init__(self, rawData: np.ndarray, chunkNr):
        self.rawData = rawData
        self.chunkFreqs, self.chunkFFT = BaseProcessingUtils.getFFT(self.rawData, Cai.frameRate)
        self.chunkNr = chunkNr
        
    def setMinMaxFreqs(self, fqs: Tuple):
        self.chunkMinFreq, self.chunksMaxFreq = fqs