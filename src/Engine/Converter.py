import audioop
import wave
import resampy
import numpy as np
from src.tools.Logger import Logger

from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai


class Converter:
    convertedFileName = "./resources/finalConvertedWAV.wav"
    
    @classmethod
    def adjustAudioFormat(self, wav):
        rawData = wav.readframes(wav.getnframes())  # Raw audio data (in bytes)
        
        if wav.getnchannels() != Cai.numberOfChannels:
            # Can cause errors if some day Cai.numberOfChannels will be more than 1
            Logger.info("Converting number of channels: {source} -> {target}".format(source=wav.getnchannels(),target=Cai.numberOfChannels))
            rawData = audioop.tomono(rawData, wav.getsampwidth(), 0.5, 0.5)
        
        if wav.getframerate() != Cai.frameRate:
            Logger.info("Resampling: {source} -> {target}".format(source=wav.getframerate(), target=Cai.frameRate))
            try:
                rawData = resampy.resample(np.fromstring(rawData, dtype=np.int16), wav.getframerate(), Cai.frameRate).tostring()
                # TODO: resample sould recieve np.ndarray :float, not np.int16
            except ValueError | TypeError as e:
                Logger.info("Resampling exception! ValueError | TypeError\n")
                raise e
                
        if wav.getsampwidth() != Cai.sampleWidthInBytes:
            Logger.info("BitDepth change: {source} -> {target}".format(source=wav.getsampwidth(), target=Cai.sampleWidthInBytes))
            rawData = audioop.lin2lin(rawData, wav.getsampwidth(), Cai.sampleWidthInBytes)
        
        wav_file = wave.open(self.convertedFileName, 'w')
        wav_file.setparams((Cai.numberOfChannels, Cai.sampleWidthInBytes, Cai.frameRate,
                            int(len(rawData) / Cai.sampleWidthInBytes), 'NONE', "not compressed"))
        wav_file.writeframes(rawData)
        wav_file.close()
        
        return wave.open(self.convertedFileName)
