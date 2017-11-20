import numpy as np
from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from typing import Tuple

class Chunk:
    def __init__(self, rawData: np.ndarray, chunkNr=None):
        
        self.rawData = rawData
        self.chunkFreqs, self.chunkFFT = BaseProcessingUtils.getFFT(self.rawData, Cai.frameRate)
        self.chunkNr = chunkNr  # TODO: delete(?)

        self.chunksMinFreq = np.min(np.abs(self.chunkFFT))
        self.chunksMaxFreq = np.max(np.abs(self.chunkFFT))
