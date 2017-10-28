import abc

class Observer(abc.ABC):
    
    @abc.abstractmethod
    def handleNewData(self, data):
        return
