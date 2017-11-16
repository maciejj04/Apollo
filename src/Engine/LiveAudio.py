from .Audio import Audio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
import numpy as np
from src.MessageServer import MessageServer, MsgTypes
from src.MessageClient import MessageClient


class LiveAudio(Audio, MessageClient):
    def __init__(self):
        Audio.__init__(self)
        MessageServer.registerForEvent(self, MsgTypes.NEW_CURRENT_CHUNK)
        
        self.fullRawAudioData: np.ndarray  # = np.ones(0, dtype=Cai.sampleWidthNumpy)
    
    def handleMessage(self, msgType, data):
        return {
            MsgTypes.NEW_CURRENT_CHUNK: self._setCurrentProcessedChunkNr(data)
        }[msgType]
