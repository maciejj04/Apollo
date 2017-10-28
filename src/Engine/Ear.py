"""
this is a stripped down version of the Ear class.
It's designed to hold only a single audio sample in memory.
"""

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


# Observer: Stream
# Observable for: ProcessingEngine
class Ear(Observable, Observer):
    """
    The Ear class is provides access to continuously recorded
    (and mathematically processed) microphone data.
    """
    
    chunkData = None  # will fill up with threaded recording data
    fft = None
    _record: bool = False
    _recordData: np.ndarray = np.ones(0, dtype=Cai.sampleWidthNumpy)
    _recordedFrames: int = 0
    stream: Stream = None
    _processingEngine: ProcessingEngine = ProcessingEngine()
    
    def __init__(self):
        
        self.pyAudio = pyaudio.PyAudio()
        Idi.currentlyUsedDeviceIndex = self.getValidDeviceIndex()
        self.setCommonAudioInformations()
        self.datax = np.arange(Cai.getChunkSize()) / float(Cai.frameRate)
        
        Logger.info("Using: {name} (device {device}) at {hz} Hz"
                    .format(name=Idi.name, device=Idi.currentlyUsedDeviceIndex, hz=Cai.frameRate))
        
        self.chunksRead = 0
    
    def getValidDeviceIndex(self):  # getvalidInputDeviceIndex?
        """ Gets first available device by default. TODO?"""
        
        mics = self.getValidInputDevices()
        return mics[0]
    
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
            device = {
                deviceIndex: info['name']
            }
            Idi.foundDevices.update(device)
        
        return mics
    
    ### STREAM HANDLING
    ### SETUP AND SHUTDOWN
    
    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.stream.close()
        self.pyAudio.terminate()
    
    def stream_start(self):
        """adds data to self.data until termination signal"""
        
        self.stream = Stream(self.pyAudio).open()
        self.stream.addObserver(self)
        
        self.stream.readChunk()
    
    # RECORDING API
    def startRecording(self):
        Logger.info("Starting recording")
        self._record = True
    
    def stopRecording(self):
        self._record = False
        Logger.info("Stopping recording. Saved {nrOfRecFrames}->{real} frames".format(nrOfRecFrames=self._recordedFrames, real=Cai.numberOfFrames))
        self._recordedFrames = 0
        self.saveRecordedDataToFile()
    
    def saveRecordedDataToFile(self, fileName='Recorded.wav'):
        waveFile = wave.open(fileName, 'wb')
        waveFile.setnchannels(Cai.numberOfChannels)
        waveFile.setsampwidth(Cai.sampleWidthInBytes)
        waveFile.setframerate(Cai.frameRate)
        waveFile.writeframes(self._recordData.tostring())
        Logger.info("Saving recorded data as: " + fileName)
        waveFile.close()
    
    # For Observer pattern__________________________________________________________________________
    def notifyObservers(self, chunkData):
        for o in self._observers:
            o.handleNewData(chunkData)
    
    # USED BY OBSERVABLE(Stream)
    def handleNewData(self, data):
        self.chunkData = data
        if self._record and self._recordedFrames < Cai.numberOfFrames:
            self._recordData = np.append(self._recordData, self.chunkData)
            # self._recordData.append(chunkData)
            self._recordedFrames += Cai.getChunkSize()
            print("_recordedFrames={}, nrOfframes = {}".format(self._recordedFrames, Cai.numberOfFrames))
        elif self._recordedFrames >= Cai.numberOfFrames:
            self._recordData = self._recordData[:Cai.numberOfFrames]
            self.stopRecording()
            
        # TODO: this should be caluculated in separate thread(?)
        self.notifyObservers(self.chunkData)

# if __name__ == "__main__":
#     ear = Ear(updatesPerSecond=10)  # optionally set sample rate here
#     ear.stream_start()  # goes forever
#     lastRead = ear.chunksRead
#     while True:
#         while lastRead == ear.chunksRead:
#             time.sleep(.01)
#         print(ear.chunksRead, len(ear.data))
#         lastRead = ear.chunksRead
#     print("DONE")
