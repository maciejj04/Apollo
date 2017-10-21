"""
this is a stripped down version of the Ear class.
It's designed to hold only a single audio sample in memory.
"""

import pyaudio
import time
import numpy as np
import threading
from src.tools.helper_functions import *
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.tools.Logger import Logger
from src.Commons.InputDeviceInfo import InputDeviceInfo as Idi


class Ear:
    """
    The Ear class is provides access to continuously recorded
    (and mathematically processed) microphone data.
    
    Arguments:
        
        device - the number of the sound card input to use. Leave blank
        to automatically detect one.
        
        updatesPerSecond - how fast to record new data. Note that smaller
        numbers allow more data to be accessed and therefore high
        frequencies to be analyzed if using a FFT later
    """
    
    def __init__(self):
        
        self.pyAudio = pyaudio.PyAudio()
        Idi.currentlyUsedDeviceIndex = self.getValidDeviceIndex()
        self.setCommonAudioInformations()
        self.datax = np.arange(Cai.getChunk()) / float(Cai.frameRate)
        
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
    
    # def valid_low_rate(self, device):
    #     """set the rate to the lowest supported audio rate."""
    #     for testrate in [44100]:
    #         if self.valid_input_device(device, testrate):
    #             return testrate
    #     print("SOMETHING'S WRONG! I can't figure out how to use DEV", device)
    #     return None
    
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
    
    ### SETUP AND SHUTDOWN
    
    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.keepRecording = False  # the threads should self-close
        while (self.threadObject.isAlive()):  # wait for all threads to close
            time.sleep(.1)
            
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()
        self.pyAudio = pyaudio.PyAudio()
    
    ### STREAM HANDLING
    
    def stream_readchunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.data = np.fromstring(self.stream.read(Cai.getChunk()), dtype=np.int16)
            self.fftx, self.fft = getFFT(self.data, Cai.frameRate)
        
        except Exception as E:
            print(" -- exception! terminating...")
            print(E, "\n" * 3)
            self.keepRecording = False
            
        if self.keepRecording:
            self.newStreamThread()
        else:
           
            print(" -- stream STOPPED")
        self.chunksRead += 1
    
    def newStreamThread(self):
        self.threadObject = threading.Thread(target=self.stream_readchunk)
        self.threadObject.start()
    
    def stream_start(self):
        """adds data to self.data until termination signal"""

        self.keepRecording = True  # set this to False later to terminate stream
        self.data = None  # will fill up with threaded recording data
        self.fft = None
        self.dataFiltered = None  # same
        self.stream = self.pyAudio.open(format=Cai.sampleWidthPyAudio, input_device_index=Idi.currentlyUsedDeviceIndex,
                                        channels=Cai.numberOfChannels, rate=Cai.frameRate, input=True,
                                        frames_per_buffer=Cai.getChunk())
        Logger.info("Opening stream based on device: "+str(Idi.currentlyUsedDeviceIndex))
        self.newStreamThread()

# if __name__ == "__main__":
#     ear = Ear(updatesPerSecond=10)  # optinoally set sample rate here
#     ear.stream_start()  # goes forever
#     lastRead = ear.chunksRead
#     while True:
#         while lastRead == ear.chunksRead:
#             time.sleep(.01)
#         print(ear.chunksRead, len(ear.data))
#         lastRead = ear.chunksRead
#     print("DONE")
