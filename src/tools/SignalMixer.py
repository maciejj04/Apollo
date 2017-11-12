import numpy as np
import pydub
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.tools.Logger import Logger

def signalMixer(data1: np.ndarray, data2: np.ndarray, saveFilePath="./mixed.wav"):
    segment1 = pydub.AudioSegment(data1, sample_width=Cai.sampleWidthInBytes, frame_rate=Cai.frameRate, channels=Cai.numberOfChannels)
    segment2 = pydub.AudioSegment(data2, sample_width=Cai.sampleWidthInBytes, frame_rate=Cai.frameRate, channels=Cai.numberOfChannels)

    combined_sounds = segment1 + segment2
    combined_sounds.export(saveFilePath, format="wav")
    Logger.info("saved mixed audio file at {}".format(saveFilePath))