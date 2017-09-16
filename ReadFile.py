from pydub.pydub import AudioSegment
import wave

def readFile( filePath, exportPath='./resources/convertedToWavResourceAudio.wav' ):
    fileToConvert = AudioSegment.from_file( filePath )
    fileToConvert.export( exportPath, format="wav")
    
    return wave.open(exportPath, 'r')
    # TODO: Check in SWEar how to wav file should be read
    # TODO: save with appropriate bitdepth samping etc.
