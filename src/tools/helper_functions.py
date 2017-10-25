import sys, os
import numpy as np
import matplotlib.pyplot as plt
import math
import wave
import struct
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.tools.Logger import Logger
from src.Commons.Audio import Audio
from src.Engine.ReadFile import readFile

def my_range(start, end, step):
    while start <= end:
        yield start if start < end else end
        start += step



def generateSampleWaveFile(filePath, fileName, freq=440.0, frameRate=44100, sampleWidth=2, nframes=40000):
    # http://stackoverflow.com/questions/3637350/how-to-write-stereo-wav-files-in-python
    # http://www.sonicspot.com/guide/wavefiles.html
    amp = 64000.0
    nchannels = 1
    framerate = int(frameRate)
    comptype = "NONE"
    compname = "not compressed"
    data = [math.sin(2 * math.pi * freq * (x / frameRate)) for x in range(nframes)]

    wav_file = wave.open(filePath + fileName, 'w')
    wav_file.setparams(
        (nchannels, sampleWidth, framerate, nframes, comptype, compname))
    for v in data:
        wav_file.writeframes(struct.pack('h', int(v * amp / 2)))
    wav_file.close()


def getInputArguments():
    return Audio.filePath if len(sys.argv) < 2 else sys.argv[1]


def getAudioFile(filePath: str=None):
    if filePath is None or filePath == "":
        filePath = getInputArguments()

    Audio.filePath = filePath
    validateFilePath(filePath)
    
    audio = readFile(filePath)
    Audio.setFields(filePath, audio.getnchannels(), audio.getsampwidth(), audio.getframerate(),
                    audio.getnframes(), audio.getcompname(), audio.getcompname())
    Cai.numberOfFrames = audio.getnframes()
    
    Logger.logAudioInfo()
    
    return audio


def validateFilePath(filePath):
    if not os.path.exists(filePath):
        Logger.info("Path to file does not exist! [{filepath}]".format(filepath=filePath))
        raise ValueError("Path to file does not exist! [{filepath}]".format(filepath=filePath))
    
    return True
