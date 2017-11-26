import numpy as np
from math import sqrt
from src.Observer import Observer
from src.Engine.helpers.NewThreadExecutionAanotation import executeInNewThread
from src.Engine.LiveAudio import LiveAudio

'''
    NOTICE:
      - accuracy of the coorelation can depend on quality of the recording! E.g.: build-in mic = ~.95, Novox nc-1 = ~.99
'''

# class is a observer. Observes if new data comes in!
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
        currChunkNr = len(liveAudio.chunks) - 1
        liveChunk = liveAudio.chunks[currChunkNr]
        statChunk = self.staticAudio.chunks[currChunkNr]
        currCorr = self.measureNormalizedCrossCorelation(statChunk.chunkFFT, liveChunk.chunkFFT)
        print("Corr {} = {}".format(currChunkNr, currCorr))
    
    def measureNormalizedCrossCorelation(self, data1: np.ndarray, data2: np.ndarray):
        def corrDenominator(dataSet1, dataSet2):
            def squareSum(dataSet):
                return sum(e * e for e in dataSet)
            
            return sqrt(squareSum(dataSet1) * squareSum(dataSet2))
        
        return (np.correlate(data1, data2) / corrDenominator(data1, data2))[0]
