import numpy as np
from math import sqrt

from src.Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


class CorrPlugin(PluginAbstractModel):
    """
    Plugin finds best fit for chunks spectrum in static audio. It is implemented by using 'moving' window.
    'Step' for the moving window is 1/10 of a window length - this is determined by computing power of device that
    application runs on. As an effect class produces vector of correlation for each window => vector of vectors.
    This is to find delays and tempo change in user version of the recording.
    In the future Plugin (or all of the plugins) should be considered for running in separete processes by reason of GIL.
    """
    # WARN! No bandpass filter for now!
    def __init__(self, windowWidth):
        super().__init__(windowWidth)
        self.corrValues: [] = []
        self.step: int = int(self.windowWidth / 10)  # TODO: Hardcoded for now. Should be set according to the application flow.
        self.staticSpectrums: [] = []
        self.liveSpectrums: [] = []
        self.liveAudioRawData: np.ndarray = np.array([])  # assume that type is float64?
        self.startIndex: int = 0
        self.correlationVectors: [] = []
        self.processSpectrumsFromRawData()
        print("dupa")

    
    def process(self, data) -> str:
        # self.liveAudioRawData = np.append(self.liveAudioRawData, data)
        # self.correlateAsFarAsYouCan()
        return "CorrPlugin handled data"
    
    # one object per single window analysis
    class NormalizedCrossCorr:
        def __init__(self, data1):
            self.squareSumSqrt = sqrt(squareSum(data1))
        
        def measureNormalizedCrossCorelation(self, data1: np.ndarray, data2: np.ndarray):
            return np.correlate(data1, data2)[0] / \
                    (self.squareSumSqrt * sqrt(squareSum(data2)))
    
    def processSpectrumsFromRawData(self):
        for i in range(0, self.staticAudioRawData.size - self.windowWidth, self.step):
            self.staticSpectrums.append(
                self._getFreqSpectrum(
                    self.staticAudioRawData[i: i + self.windowWidth]
                )
            )
    
    def _getFreqSpectrum(self, data: np.ndarray) -> np.ndarray:
        data = data * np.hamming(len(data))  # TODO: Give user a choice!
        freqSpectrum = abs(np.fft.fft(data))  # Can be optimized
        
        return freqSpectrum[:int(len(freqSpectrum) / 2)]
    
    def correlateAsFarAsYouCan(self):
        for i in range(self.startIndex, self.liveAudioRawData.size - self.windowWidth, self.step):
            
            spectrum = self._getFreqSpectrum(self.liveAudioRawData[i:i + self.windowWidth])
            
            self.liveSpectrums.append(spectrum)
            self._compareWithEachStaticSpectrum(spectrum)
            
            self.startIndex += self.step

    def _compareWithEachStaticSpectrum(self, spectrum: np.ndarray):
        corr = CorrPlugin.NormalizedCrossCorr(spectrum)
        corrVector = []
        for j in range(0, len(self.staticSpectrums)):
            corrVector.append(
                corr.measureNormalizedCrossCorelation(
                    spectrum, self.staticSpectrums[j]
                )
            )
        self.correlationVectors.append(corrVector)


def squareSum(dataSet):
    return sum(e * e for e in dataSet)