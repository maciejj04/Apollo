import numpy as np
from math import sqrt
from src.Observer import Observer
from src.Engine.helpers.NewThreadExecutionAanotation import executeInNewThread
from src.Engine.LiveAudio import LiveAudio
from src.tools.Logger import Logger
from  scipy import stats
from src.MessageServer import MessageServer
'''
    NOTICE:
      - accuracy of the coorelation can depend on the quality of the recording! E.g.: build-in mic = ~.95, Novox nc-1 = ~.99
'''

class InterpretEngine(Observer):
    def __init__(self, staticAudioRef):
        Observer.__init__(self)
        self.staticAudio = staticAudioRef
    
    def handleNewData(self, data):
        '''
        :param data: liveAudio Reference
        :return: void
        '''
        self.interpret(data)

    @executeInNewThread
    def interpret(self, liveAudio: LiveAudio):
        chunksCorr = self.measureNormalizedCrossCorelationFromAudio(liveAudio)
        hzDiff = self.baseHzAbsoluteDifference(liveAudio)
        
        statChunk, liveChunk = self._getCurrentCorrespondingChunks(liveAudio)
        pearsonPCMCorr = self.pearsonCorrelationCoefficient(statChunk.rawData, liveChunk.rawData)
        pearsonSpectrumCorr = self.pearsonCorrelationCoefficient(statChunk.chunkFFT, liveChunk.chunkFFT)
        
        Logger.interpretEngineLog("""[{chunkNr}] corr = {corr}
                        HzDiff = {HzDiff}
                        PerasonPCMCorr = {pearsonPCMCorr}
                        pearsonSpectrumCorr = {pearsonSpectrumCorr}
                        """
                        .format(chunkNr=liveAudio.getLastChunksIndex()-1, corr=chunksCorr, HzDiff=hzDiff,
                                pearsonPCMCorr=pearsonPCMCorr,pearsonSpectrumCorr=pearsonSpectrumCorr))
        
    
    # can be extracted as a plugin
    def measureNormalizedCrossCorelationFromAudio(self, liveAudio: LiveAudio):
        def measureNormalizedCrossCorelation(data1: np.ndarray, data2: np.ndarray):
            def corrDenominator(dataSet1, dataSet2):
                def squareSum(dataSet):
                    return sum(e * e for e in dataSet)
            
                return sqrt(squareSum(dataSet1) * squareSum(dataSet2))
        
            return (np.correlate(data1, data2) / corrDenominator(data1, data2))[0]
     
        staticChunk, liveChunk = self._getCurrentCorrespondingChunks(liveAudio)
        return measureNormalizedCrossCorelation(data1=staticChunk.chunkFFT, data2=liveChunk.chunkFFT)
    
    def baseHzAbsoluteDifference(self, liveAudio: LiveAudio):
        currChunkNr = len(liveAudio.chunks) - 1
        staticHz = self.staticAudio.frequencyEnvelope[currChunkNr]
        liveHz = liveAudio.getFrequencyEnvelope()[currChunkNr]
        # TODO: display the difference on HzDiff LCD
        return abs(staticHz - liveHz)
    
    def pearsonCorrelationCoefficient(self, dataSet1: np.ndarray, dataSet2: np.ndarray):
        return stats.pearsonr(dataSet1, dataSet2)[0]
    
    def _getCurrentCorrespondingChunks(self, liveAudio: LiveAudio) -> ():
        currChunkNr = len(liveAudio.chunks) - 1
        liveChunk = liveAudio.chunks[currChunkNr]
        statChunk = self.staticAudio.chunks[currChunkNr]
        return statChunk, liveChunk