import numpy as np
import matplotlib.pyplot as plt
import math
import wave
import struct

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
    plt.plot(freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)])
    plt.show()
    return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


def generateSampleWaveFile():
    # http://stackoverflow.com/questions/3637350/how-to-write-stereo-wav-files-in-python
    # http://www.sonicspot.com/guide/wavefiles.html
    freq = 440.0
    fname = "test.wav"
    frate = 11025.0
    amp = 64000.0
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = 40000
    comptype = "NONE"
    compname = "not compressed"
    data = [math.sin(2 * math.pi * freq * (x / frate)) for x in range(nframes)]
    print(len(data))
    print(data[100])
    wav_file = wave.open(fname, 'w')
    wav_file.setparams(
        (nchannels, sampwidth, framerate, nframes, comptype, compname))
    for v in data:
        wav_file.writeframes(struct.pack('h', int(v * amp / 2)))
    wav_file.close()
    
def findHighestFreq():
    nframes = 40000
    fname = "test.wav"
    frate = 11025.0
    wav_file = wave.open(fname, 'r')
    data = wav_file.readframes(nframes)
    wav_file.close()
    data = struct.unpack('{n}h'.format(n=nframes), data)
    data = np.array(data)

    w = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(w))
    print(freqs.min(), freqs.max())
    # (-0.5, 0.499975)

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * frate)
    print(freq_in_hertz)
    # 439.8975