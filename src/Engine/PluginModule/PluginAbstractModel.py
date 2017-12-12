import abc
import numpy as np


class PluginAbstractModel(abc.ABC):

    staticAudioRawData: np.ndarray
    
    @abc.abstractmethod
    def process(self, data) -> str:
        pass
