from typing import Tuple

import numpy as np
from math import sqrt

from src.Commons.Settings import TOP_FREQS_COUNT
from src.Observer import Observer
from src.Engine.helpers.NewThreadExecutionAanotation import executeInNewThread
from src.Engine.LiveAudio import LiveAudio
from src.tools.Logger import Logger
from scipy import stats
from src.MessageServer import MessageServer

'''
    NOTICE:
      - accuracy of the coorelation depend on the quality of the recording! E.g.: build-in mic = ~.95, Novox nc-1 = ~.99
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
        self.staticChunk, self.liveChunk = self._getCurrentCorrespondingChunks(liveAudio)

        chunksCorr = self.measureNormalizedCrossCorelationFromAudio(liveAudio)
        hzDiff = self.baseHzAbsoluteDifference(liveAudio)
        
        pearsonPCMCorr = self.pearsonCorrelationCoefficient(self.staticChunk.rawData, self.liveChunk.rawData)
        pearsonSpectrumCorr = self.pearsonCorrelationCoefficient(self.staticChunk.chunkAS, self.liveChunk.chunkAS)
        diffsTuple = self.compareNHighestAmplitudes(liveAudio)

        Logger.interpretEngineLog("""[{chunkNr}] corr = {corr}
                        HzDiff = {HzDiff}
                        PerasonPCMCorr = {pearsonPCMCorr}
                        pearsonSpectrumCorr = {pearsonSpectrumCorr}
                        TopFreqsDiffs = {diffs}
                        """.format(chunkNr=liveAudio.getLastChunksIndex() - 1, corr=chunksCorr, HzDiff=hzDiff,
                                          pearsonPCMCorr=pearsonPCMCorr, pearsonSpectrumCorr=pearsonSpectrumCorr,
                                          diffs=diffsTuple))

        self.compareSpectrumCentroid()
    
    # can be extracted as a plugin
    def measureNormalizedCrossCorelationFromAudio(self, liveAudio: LiveAudio):
        def measureNormalizedCrossCorelation(data1: np.ndarray, data2: np.ndarray):
            def corrDenominator(dataSet1, dataSet2):
                def squareSum(dataSet):
                    return sum(e * e for e in dataSet)
                
                return sqrt(squareSum(dataSet1) * squareSum(dataSet2))
            
            return (np.correlate(data1, data2) / corrDenominator(data1, data2))[0]
            
        staticChunk, liveChunk = self._getCurrentCorrespondingChunks(liveAudio)
        return measureNormalizedCrossCorelation(data1=staticChunk.chunkAS, data2=liveChunk.chunkAS)
    
    def baseHzAbsoluteDifference(self, liveAudio: LiveAudio):
        staticChunk, liveChunk = self._getCurrentCorrespondingChunks(liveAudio)
        
        # for e in self.staticAudio.frequencyEnvelope:
        #     print("Freq{currChNr}: {val}".format(currChNr=currChunkNr, val=self.staticAudio.frequencyEnvelope[0][currChunkNr]))
        
        # TODO: display the difference on HzDiff LCD
        return abs(staticChunk.baseFrequency - liveChunk.baseFrequency)
    
    def pearsonCorrelationCoefficient(self, dataSet1: np.ndarray, dataSet2: np.ndarray):
        return stats.pearsonr(dataSet1, dataSet2)[0]  # TODO: evaluate second return-tuple element!
    
    def _getCurrentCorrespondingChunks(self, liveAudio: LiveAudio) -> ():
        currChunkNr = len(liveAudio.chunks) - 1
        liveChunk = liveAudio.chunks[currChunkNr]
        statChunk = self.staticAudio.chunks[currChunkNr]
        return statChunk, liveChunk
    
    def compareSpectrumCentroid(self):
        diff = abs(self.staticChunk.spectralCentroid - self.liveChunk.spectralCentroid)
        Logger.centroidLog("StatCentroid={}\tliveCentroid={}\tdiff={}".format(self.staticChunk.spectralCentroid, self.liveChunk.spectralCentroid, diff))

    def compareNHighestAmplitudes(self, liveAudio: LiveAudio) -> Tuple:
        processedChunkIndex = len(liveAudio.chunks) - 1
        liveAudioHighest = [liveAudio.nfrequencyEnvelopes[i][processedChunkIndex] for i in range(0, TOP_FREQS_COUNT)]
        statAudioHighest = [self.staticAudio.nfrequencyEnvelopes[i][processedChunkIndex] for i in range(0, TOP_FREQS_COUNT)]
        
        diffsTuple = tuple([abs(statAudioHighest[i] - liveAudioHighest[i]) for i in range(0, TOP_FREQS_COUNT)])
        
        return diffsTuple
