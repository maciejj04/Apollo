import abc
import numpy as np


class PluginAbstractModel(abc.ABC):

    staticAudioRawData: np.ndarray
    def __init__(self, windowWidth):
        self.windowWidth = windowWidth


    @abc.abstractmethod
    def process(self, data) -> str:
        pass
