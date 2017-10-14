import audioop
import wave

from src.Commons.Audio import Audio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


class Converter:
    inAudio = Audio()
    out = Cai()
    
    def __init__(self):
        pass
    
    def __init__(self, inAudio, out):
        self.inAudio = inAudio
        self.out = out
    
    @classmethod
    def adjustAudioFormat(self, wav):
        rad = wav.readframes(wav.getnframes())  # Raw audio data (in bytes)
        
        if wav.getnchannels() != Cai.numberOfChannels:
            # Can cause errors if some day Cai.numberOfChannels will be more than 1
            rad = audioop.tomono(rad, wav.getsampwidth(), 0.5, 0.5)  # takes half of left and right chanel
        
        if wav.getframerate() != Cai.frameRate:
            # TODO: Error prone!  ratecv() returns a TUPLE!!!!!!!!!!!!!!!!
            rad, _ratecvt = audioop.ratecv(rad, wav.getsampwidth(), Cai.numberOfChannels, wav.getframerate(),
                                           Cai.frameRate,
                                           None)
        
        if wav.getsampwidth() != Cai.sampleWidthInBytes:
            rad = audioop.lin2lin(rad, wav.getsampwidth(), Cai.sampleWidthInBytes)
        
        wav_file = wave.open('./resources/finalConvertedWAV.wav', 'w')
        wav_file.setparams((Cai.numberOfChannels, Cai.sampleWidthInBytes, Cai.frameRate,
                            int(len(rad) / Cai.sampleWidthInBytes), 'NONE', "not compressed"))
        wav_file.writeframes(rad)
        wav_file.close()
        
        return wave.open('./resources/finalConvertedWAV.wav')
