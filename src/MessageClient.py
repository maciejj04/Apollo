from abc import abstractmethod

class MessageClient:
    
    @abstractmethod
    def handleMessage(self, msgType, data):
        pass
