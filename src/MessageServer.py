from enum import Enum


class MsgTypes(Enum):
    NEW_RECORDING = 1,
    UPDATE_PCM_CHART = 2,
    NEW_CURRENT_CHUNK = 3,
    ROCORDING_STOP = 4,
    ROCORDING_PAUSE = 5


class MessageServer:
    _observers: list = []
    _observersByEvents: dict = {
        MsgTypes.NEW_RECORDING: [],
        MsgTypes.UPDATE_PCM_CHART: [],
        MsgTypes.NEW_CURRENT_CHUNK: [],  # Use only during recording
        
    }
    
    @classmethod
    def register(self, obj):
        self._observers.append(obj)
    
    @classmethod
    def registerForEvent(cls, obj, eventType: MsgTypes):
        cls._observersByEvents.get(eventType).append(obj)
    
    @classmethod
    def unRegister(self, obj):
        self._observers.remove(obj)
    
    @classmethod
    def notifyClients(self, msgType: MsgTypes, data=None):
        for i in self._observers:
            i.handleMessage(msgType=msgType, data=data)
    
    @classmethod
    def notifyEventClients(self, msgType: MsgTypes, data=None):
        for i in self._observersByEvents.get(msgType):
            i.handleMessage(msgType=msgType, data=data)
