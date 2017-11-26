import numpy as np
from math import sqrt
from src.Observer import Observer
from src.Engine.helpers.NewThreadExecutionAanotation import executeInNewThread
from src.Engine.LiveAudio import LiveAudio
from src.tools.Logger import Logger
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
        Logger.interpretEngineLog("[{chunkNr}] corr = {corr}".format(chunkNr=liveAudio.getLastChunk(), corr=chunksCorr))
    
    # can be extracted as a plugin
    def measureNormalizedCrossCorelationFromAudio(self, liveAudio: LiveAudio):
        def measureNormalizedCrossCorelation(data1: np.ndarray, data2: np.ndarray):
            def corrDenominator(dataSet1, dataSet2):
                def squareSum(dataSet):
                    return sum(e * e for e in dataSet)
            
                return sqrt(squareSum(dataSet1) * squareSum(dataSet2))
        
            return (np.correlate(data1, data2) / corrDenominator(data1, data2))[0]
     
        currChunkNr = len(liveAudio.chunks) - 1
        liveChunk = liveAudio.chunks[currChunkNr]
        statChunk = self.staticAudio.chunks[currChunkNr]
        return measureNormalizedCrossCorelation(data1=statChunk.chunkFFT, data2=liveChunk.chunkFFT)
    
