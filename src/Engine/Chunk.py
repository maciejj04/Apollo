import numpy as np
from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from typing import Tuple

class Chunk:
    def __init__(self, rawData: np.ndarray, chunkNr=None):
        
        self.rawData = rawData
        self.chunkFreqs, self.chunkAS = BaseProcessingUtils.getAplitudeSpectrum(self.rawData, Cai.frameRate) #AS - AmplitudeSpectrum
        self.chunkNr = chunkNr  # TODO: delete(?)

        self.chunksMinFreq = np.min(np.abs(self.chunkAS))
        self.chunksMaxFreq = np.max(np.abs(self.chunkAS))
