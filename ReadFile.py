from pydub.pydub import AudioSegment
import wave
import audioop
from CommonAudioInfo import CommonAudioInfo as Cai

#TODO: workaround for now. If commented, pydub says that he could not find file(if mp3 comes as parameter).
#  change to ./dependencies/ directory
AudioSegment.converter = r"C:\tools\ffmpeg-3.3.3-win64-static\ffmpeg-3.3.3-win64-static\bin\ffmpeg.exe"


def readFile(filePath, exportPath='./tmp/basicConvertedToWavResourceAudio.wav'):
    fileToConvert = AudioSegment.from_file(filePath)
    #TODO: why pydub automatically converts 4byte width frame to 2byte while converting from mp3 to wav
    fileToConvert.export(out_f=exportPath, format="wav")

    wav = wave.open(exportPath, 'r')
    
    return validateAudioParameters(wav)
    # TODO: Check in SWEar how to wav file should be read
    # TODO: save with appropriate bitdepth sampling etc.


def validateAudioParameters(wav):

    rad = wav.readframes(wav.getnframes())  #  Raw audio data (in bytes)
    if wav.getframerate() != Cai.frameRate:
        # TODO: Error prone!  ratecv() returns a TUPLE!!!!!!!!!!!!!!!!
        rad = audioop.ratecv(rad, wav.getsampwidth(), Cai.numberOfChannels, wav.getframerate(), Cai.frameRate, None)
        
    if wav.getsampwidth() != Cai.sampleWidthInBytes:
        
        rad = audioop.lin2lin(rad, wav.getsampwidth(), Cai.sampleWidthInBytes)
        
    if wav.getnchannels() != Cai.numberOfChannels:
        # Can cause errors if some day Cai.numberOfChannels will be more than 1
        rad = audioop.tomono(rad, wav.getsampwidth(), 0.5, 0.5)#remains both channels with the same volume
        
    wav_file = wave.open('./resources/finalConvertedWAV.wav', 'w')
    wav_file.setparams((Cai.numberOfChannels, Cai.sampleWidthInBytes, Cai.frameRate, int(len(rad)/Cai.sampleWidthInBytes), 'NONE', "not compressed"))
    wav_file.writeframes(rad)
    wav_file.close()
    
    return wave.open('./resources/finalConvertedWAV.wav')

