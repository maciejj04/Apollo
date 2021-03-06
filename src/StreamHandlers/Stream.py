from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.Commons.InputDeviceInfo import InputDeviceInfo as Idi
from src.tools.Logger import Logger
import threading
import time
import numpy as np
from src.Observable import Observable
from src.Engine.helpers.NewThreadExecutionAanotation import executeInNewThread
import gc
import pyaudio


class Stream(Observable):
    def __init__(self, pyAudioObj, inputDeviceIndex=Idi.currentlyUsedDeviceIndex):
        Observable.__init__(self)
        self.inputDeviceIndex = inputDeviceIndex
        self.pyAudio = pyAudioObj
        self._stream = None
        self.keepListening: bool = True
        self.data = None
    
    def open(self):
        self._stream = self.pyAudio.open(format=Cai.sampleWidthPyAudio, input_device_index=Idi.currentlyUsedDeviceIndex,
                                         channels=Cai.numberOfChannels, rate=Cai.frameRate, input=True,
                                         frames_per_buffer=Cai.getChunkSize())
        
        Logger.info("Opening stream based on device: " + str(Idi.currentlyUsedDeviceIndex))
        self.keepListening = True
        return self
    
    def close(self):
        self.keepListening = False  # the threads should self-close
        while (self.threadObject.isAlive()):  # wait for all threads to close
            time.sleep(.1)
        
        self._stream.stop_stream()
        self._stream.close()
    
    def readChunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.data = np.fromstring(self._stream.read(Cai.getChunkSize()), dtype=np.int16)
            self.notifyObservers(self.data)
        
        except Exception as E:
            print(" -- exception! terminating...")
            print(E, "\n" * 3)
            self.keepListening = False
        
        if self.keepListening:
            self._newStreamThread()
        else:
            print(" -- stream STOPPED")
    
    def _newStreamThread(self):
        self.threadObject = threading.Thread(target=self.readChunk)
        self.threadObject.start()
    
    def notifyObservers(self, data):
        for o in self._observers:
            o.handleNewData(data)
