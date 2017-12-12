import abc


class PluginAbstractModel(abc.ABC):
    
    @abc.abstractmethod
    def process(self, data) -> str:
        pass
