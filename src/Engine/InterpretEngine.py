import struct
import numpy as np
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from typing import Tuple
# import scipy.fftpack as sf
from .ProcessingEngine import ProcessingEngine


# class is a observer. Observes if new data comes in!
class InterpretEngine:
    _loadedFilePE: ProcessingEngine = None
    _inputStreamPE: ProcessingEngine = None
    
    def __init__(self):
        pass
    
    def handleNewData(self):
        pass
    
    def _getPCMDiffrences(self):
        pass
