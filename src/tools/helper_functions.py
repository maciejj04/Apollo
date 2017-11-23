import sys, os
import numpy as np
import matplotlib.pyplot as plt
import math
import wave
import struct
#from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

def my_range(start, end, step):
    while start <= end:
        yield start if start < end else end
        start += step


def generateSampleFreqRawData(freq=440.0, frameRate=44100, sampleWidth=2, nframes=40000, sec=None):
    if sec is not None:
        nframes = frameRate*sec
        
    return [math.sin(2 * math.pi * freq * (x / frameRate)) for x in range(nframes)]


def generateSampleWaveFile(filePath, fileName, freq=440.0, frameRate=44100, sampleWidth=2, nframes=40000):
    # http://stackoverflow.com/questions/3637350/how-to-write-stereo-wav-files-in-python
    # http://www.sonicspot.com/guide/wavefiles.html
    amp = 64000.0
    nchannels = 1
    framerate = int(frameRate)
    comptype = "NONE"
    compname = "not compressed"
    data220 = generateSampleFreqRawData(freq=220, sec=4)
    data440 = generateSampleFreqRawData(freq=440, sec=4)
    
    wav_file = wave.open(filePath + fileName, 'w')
    wav_file.setparams(
        (nchannels, sampleWidth, framerate, frameRate*12, comptype, compname))
    for v in data220:
        wav_file.writeframes(struct.pack('h', int(v * amp / 2)))

    for i in range(len(data440)):
        wav_file.writeframes(struct.pack('h', int(0)))

    for v in data440:
        wav_file.writeframes(struct.pack('h', int(v * amp / 2)))
    
    wav_file.close()


generateSampleWaveFile("./", "220_pause_440_12s.wav")