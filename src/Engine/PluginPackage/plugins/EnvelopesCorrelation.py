import numpy as np
from math import sqrt


class EnvelopesCorrelation:
    def __init__(self, env1, env2, windowSize, step=None):
        self.env1 = env1
        self.env2 = env2
        self.windowSize = windowSize
        if step is None:
            self.step = int(self.windowSize / 10)
        else:
            self.step = step
    
    def correlate(self):
        corrVectors = []
        for i in range(0, len(self.env1) - self.windowSize + 1, self.step):
            corrVectors.append([])
            data1 = self.env1[i: i + self.step]
            corr = EnvelopesCorrelation.NormalizedCrossCorr(data1)
            for j in range(0, len(self.env2) - self.windowSize + 1, self.step):
                corrVectors[len(corrVectors) - 1].append(
                    corr.measureNormalizedCrossCorelation(data1=data1,
                                                          data2=self.env2[j:j + self.windowSize])
                )

        self.print3DPlot(corrVectors)
    
    class NormalizedCrossCorr:
        def __init__(self, data1):
            self.squareSumSqrt = sqrt(squareSum(data1))
        
        def measureNormalizedCrossCorelation(self, data1: np.ndarray, data2: np.ndarray):
            return np.correlate(data1, data2)[0] / \
                   (self.squareSumSqrt * sqrt(squareSum(data2)))
    
    def print3DPlot(self, arrayOfArrays):
        import matplotlib.pyplot as plt
        im = plt.imshow(arrayOfArrays, cmap='hot')
        plt.colorbar(im, orientation='horizontal')
        plt.show()


def squareSum(dataSet):
    return sum(e * e for e in dataSet)
