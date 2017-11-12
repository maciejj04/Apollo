import pyaudio
from src.tools.Logger import Logger


def validateOutputDevices(pyAudio: pyaudio.PyAudio()):
    validDevicesIndexes = []
    for deviceIndex in range(pyAudio.get_device_count()):
        devInfo = pyAudio.get_device_info_by_index(deviceIndex)
        if devInfo["maxOutputChannels"] > 0:
            validDevicesIndexes.append(deviceIndex)
    
    Logger.info("Found {listLen} valid output devices".format(listLen=len(validDevicesIndexes)))
    return validDevicesIndexes
