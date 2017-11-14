import abc


class MessageClient(abc.ABC):
    @abc.abstractmethod
    def handleMessage(self, msgType, data):
        pass
