import numpy as np
import matplotlib.pyplot as plt
import math
import wave
import struct
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


def getFFT(data, rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    data = data * np.hamming(len(data))
    fft = np.fft.fft(data)
    fft = np.abs(fft)
    # fft=10*np.log10(fft)
    freq = np.fft.fftfreq(len(fft), 1.0 / rate)
    # plt.plot(freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)])
    # plt.show()
    return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


def generateSampleWaveFile(filePath, fileName, freq=440.0, frameRate=44100, sampleWidth=2, nframes=40000):
    # http://stackoverflow.com/questions/3637350/how-to-write-stereo-wav-files-in-python
    # http://www.sonicspot.com/guide/wavefiles.html
    amp = 64000.0
    nchannels = 1
    framerate = int(frameRate)
    comptype = "NONE"
    compname = "not compressed"
    data = [math.sin(2 * math.pi * freq * (x / frameRate)) for x in range(nframes)]
    print(len(data))
    print(data[100])
    wav_file = wave.open(filePath + fileName, 'w')
    wav_file.setparams(
        (nchannels, sampleWidth, framerate, nframes, comptype, compname))
    for v in data:
        wav_file.writeframes(struct.pack('h', int(v * amp / 2)))
    wav_file.close()
    
    



