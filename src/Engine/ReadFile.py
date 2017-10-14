from pydub import AudioSegment
import wave
from src.Engine.Converter import Converter
import audioop
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai

# TODO: workaround for now. If commented, pydub says that he could not find file(if mp3 comes as parameter).
#  change to ./dependencies/ directory
AudioSegment.converter = r"C:\tools\ffmpeg-3.3.3-win64-static\ffmpeg-3.3.3-win64-static\bin\ffmpeg.exe"


def readFile(filePath, exportPath='./tmp/basicConvertedToWavResourceAudio.wav'):
    fileToConvert = AudioSegment.from_file(filePath)
    # TODO: why pydub automatically converts 4byte width frame to 2byte while converting from mp3 to wav
    fileToConvert.export(out_f=exportPath, format="wav")
    
    wav = wave.open(exportPath, 'r')
    
    return Converter.adjustAudioFormat(wav)
    # TODO: Check in Ear how to wav file should be read
    # TODO: save with appropriate bitdepth sampling etc.
