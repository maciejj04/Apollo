from enum import Enum


class MsgTypes(Enum):
    NEW_RECORDING = 1,
    UPDATE_PCM_CHART = 2
    

class MessageServer:
    _observers: list = []
    _observersDict: dict = {
                                MsgTypes.NEW_RECORDING: [],
                                MsgTypes.UPDATE_PCM_CHART: []
    }# TODO: correct var name, not valueable according to CleanCode
    
    
    @classmethod
    def register(self, obj):
        self._observers.append(obj)
        
    @classmethod
    def registerForEvent(cls, obj, eventType: MsgTypes):
        cls._observersDict.get(eventType).append(obj)

    @classmethod
    def unRegister(self, obj):
        self._observers.remove(obj)

    @classmethod
    def notifyClients(self, msgType: MsgTypes, data=None):
        for i in self._observers:
            i.handleMessage(msgType=msgType, data=data)

    @classmethod
    def notifyEventClients(self, msgType: MsgTypes, data=None):
        for i in self._observersDict.get(msgType):
            i.handleMessage(msgType=msgType, data=data)
