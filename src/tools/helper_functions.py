import sys, os
import numpy as np
import matplotlib.pyplot as plt
import math
import wave
import struct
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.Engine.ReadFile import getRawAudioFramesFromFile

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


