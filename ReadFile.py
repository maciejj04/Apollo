from pydub.pydub import AudioSegment
import wave
import audioop
from CommonAudioInfo import CommonAudioInfo as Cai

#TODO: workaround for now. If commented, pydub says that he could not find file(if mp3 comes as parameter).
#TODO: change to ./dependencies/ directory
AudioSegment.converter = r"C:\tools\ffmpeg-3.3.3-win64-static\ffmpeg-3.3.3-win64-static\bin\ffmpeg.exe"

def readFile(filePath, exportPath='./resources/convertedToWavResourceAudio.wav'):
    fileToConvert = AudioSegment.from_file(filePath, format='wav')
    fileToConvert.export(out_f=exportPath, format="wav")

    wav = wave.open(exportPath, 'r')
    converted = validateAudioParameters(wav)
    
    return converted
    # TODO: Check in SWEar how to wav file should be read
    # TODO: save with appropriate bitdepth sampling etc.


def validateAudioParameters(wav):
    import copy
    rad = wav.readframes(wav.getnframes())  #  Raw audio data ( in bytes )
    if wav.getframerate() != Cai.frameRate:
        rad = audioop.ratecv(rad, wav.getnframes(), Cai.numberOfChannels, wav.getframerate(), Cai.frameRate, None)
        
    if wav.getsampwidth() != Cai.sampleWidthInBytes:
        rad = audioop.lin2lin(rad, wav.getsampwidth(), Cai.sampleWidthInBytes)
        
    if wav.getnchannels() != Cai.numberOfChannels:
        # Can cause errors if some day Cai.numberOfChannels will be more than 1
        rad = audioop.tomono(rad, wav.getsampwidth(), 0.5, 0.5)#remains both channels with the same volume
        
    wav_file = wave.open('./finalWAV.wav', 'w')
    wav_file.setparams((Cai.numberOfChannels, Cai.sampleWidthInBytes, Cai.frameRate, int(len(rad)/Cai.sampleWidthInBytes), 'NONE', None))
    wav_file.writeframes(rad)
    wav_file.close()
    
    return wave.open('./finalWAV.wav')

