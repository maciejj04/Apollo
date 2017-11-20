import pyaudio
import time
import numpy as np
from src.tools.helper_functions import *
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.tools.Logger import Logger
from src.Commons.InputDeviceInfo import InputDeviceInfo as Idi
from src.StreamHandlers.Stream import Stream
from src.Engine.ProcessingEngine import ProcessingEngine
from src.Observable import Observable, Observer
from src.MessageServer import MessageServer, MsgTypes

# Observer: Stream
# Observable for: ProcessingEngine
class Ear():
    """
    The Ear class provides access to continuously recorded microphone data.
    """
    
    chunkData = None  # will fill up with threaded recording data
    fft = None
    _record: bool = False
    _recordData: np.ndarray = np.ones(0, dtype=Cai.sampleWidthNumpy)
    _recordedFrames: int = 0
    stream: Stream = None
    
    def __init__(self):
        Observable.__init__(self)
        Observer.__init__(self)
        self.pyAudio = pyaudio.PyAudio()
        Idi.currentlyUsedDeviceIndex = self.getValidDeviceIndex()
        self.setCommonAudioInformations()
        self.datax = np.arange(Cai.getChunkSize()) / float(Cai.frameRate)
        
        Logger.info("Using: {name} (device {device}) at {hz} Hz"
                    .format(name=Idi.name, device=Idi.currentlyUsedDeviceIndex, hz=Cai.frameRate))
        
        self.chunksRead = 0
        self.stream = Stream(self.pyAudio)
    
    def getValidDeviceIndex(self):  # getvalidInputDeviceIndex?
        """ Gets first available device by default."""
        
        mics = self.getValidInputDevices()
        return mics[1] if len(mics) > 1 else mics[0]
    
    def setCommonAudioInformations(self):
        info = self.pyAudio.get_device_info_by_index(Idi.currentlyUsedDeviceIndex)
        Cai.frameRate = int(info["defaultSampleRate"])
        Idi.name = Idi.foundDevices.get(Idi.currentlyUsedDeviceIndex)
        Logger.logCommonAudioInformations()
        # TODO: check whether is the way to get to know default sample width of the input microphone device
    
    ### SYSTEM TESTS
    
    def validInputDevice(self, deviceIndex, rate=44100):
        """given a device ID and a rate, return TRUE/False if it's valid."""
        try:
            info = self.pyAudio.get_device_info_by_index(deviceIndex)
            if info["maxInputChannels"] == 0:
                return False
            
            stream = self.pyAudio.open(format=pyaudio.paInt16, channels=1,
                                       input_device_index=deviceIndex,  # , frames_per_buffer=self.chunk
                                       rate=int(info["defaultSampleRate"]), input=True)
            
            stream.close()
            return True
        except ValueError as e:
            Logger.info("ValueError Exception Occured: I/O error({0}): {1}".format(e.errno, e.strerror))
            return False
    
    def getValidInputDevices(self):
        """
        See which devices can be opened for microphone input.
        call this when no PyAudio object is loaded.
        """
        mics = []
        for device in range(self.pyAudio.get_device_count()):
            if self.validInputDevice(device):
                mics.append(device)
        if len(mics) == 0:
            print("no microphone devices found!")
        else:
            print("found %d microphone devices: %s" % (len(mics), mics))
        
        Idi.foundDevices.clear()
        
        for deviceIndex in mics:
            info = self.pyAudio.get_device_info_by_index(deviceIndex)
            device = {deviceIndex: info['name']}
            Idi.foundDevices.update(device)
        
        return mics
    
    ### STREAM HANDLING
    ### SETUP AND SHUTDOWN
    
    def close(self):
        """gently detach from things."""
        Logger.info(" -- sending stream termination command...")
        self.stream.close()
        self.pyAudio.terminate()
    
    def stream_start(self):
        """adds data to self.data until termination signal"""
        self.setCommonAudioInformations()
        if self.stream is not None:
            self.stream.open()
        else:
            raise ValueError("Stream is none (in Ear)")
        
        self.stream.readChunk()
        
    # For Observer pattern__________________________________________________________________________
    
    # def notifyObservers(self, chunkData):
    #     for o in self._observers:
    #         o.handleNewData(chunkData, shouldSave=self._record)
    #
    # # USED BY OBSERVABLE(Stream)
    # def handleNewData(self, data):
    #     self.chunkData = data
    #     if self._record and self._recordedFrames < Cai.numberOfFrames:
    #         self._recordData = np.append(self._recordData, self.chunkData)
    #         self._recordedFrames += Cai.getChunkSize()
    #     elif self._recordedFrames >= Cai.numberOfFrames:
    #         self._recordData = self._recordData[:Cai.numberOfFrames]
    #         self.stopRecording()
    #
    #     # TODO: this should be caluculated in separate thread(?)
    #     self.notifyObservers(self.chunkData)
