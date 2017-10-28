from pydub import AudioSegment
import numpy as np
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

# TODO: workaround for now. If commented, pydub says that he could not find file(if mp3 comes as parameter).
#  change to ./dependencies/ directory
AudioSegment.converter = r"C:\tools\ffmpeg-3.3.3-win64-static\ffmpeg-3.3.3-win64-static\bin\ffmpeg.exe"


def getRawAudioFramesFromFile(filePath,):

    Converter.adjustAudioFormat(wav)
    
    return np.fromstring(Converter.getRawDataFromConvertedFile(), dtype=np.int16)
    # TODO: Check in Ear how to wav file should be read
    # TODO: save with appropriate bitdepth sampling etc.
