import numpy as np
from .BaseProcessingUtils import BaseProcessingUtils
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

class Chunk:
    def __init__(self, rawData: np.ndarray, chunkNr=None):
        
        self.rawData = rawData
        self.chunkFreqs, self.chunkAS = BaseProcessingUtils.getAplitudeSpectrum(self.rawData, Cai.frameRate) #AS - AmplitudeSpectrum
        self.chunkNr = chunkNr  # TODO: delete(?)
        from src.Engine.ProcessingEngine import ProcessingEngine
        self.spectralCentroid = ProcessingEngine.calculateSpectralCentroid(self.chunkAS, self.chunkFreqs)

        self.chunksMinFreq = np.min(np.abs(self.chunkAS))  # Rename! It's not freq but just max SA value
        self.chunksMaxFreq = np.max(np.abs(self.chunkAS))
