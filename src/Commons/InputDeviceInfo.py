class InputDeviceInfo:
    # TODO: check whether it can be stored in CommonAudioInfo class or as some settings.
    currentlyUsedDeviceIndex = 0  # defines which device returned by PyAudio to use. Can be changed by options->change microphone view
    foundDevices = []
