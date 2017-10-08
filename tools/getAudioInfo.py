import sys
sys.path.append('../pydub/')
from pydub.pydub import AudioSegment

def getAudioFileInformations(filePath):
    file = AudioSegment.from_file(filePath)
    
    print("""- framerate: {}
            - nchannels: {}
            - sampwidth {}( in bytes)
            - frameCount: {}
            """\
        .format(file.frame_rate, file.channels, file.sample_width, file.frame_count()))
    
    
getAudioFileInformations('./resources/220_440.wav')
