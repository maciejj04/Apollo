import sys

from PyQt4 import QtGui

from App import App
from Logger import Logger
from ReadFile import readFile
from drawOnce import drawOnce
from Audio import Audio


def hasInputArguments():
    pass


def getAudioFile():
    # TODO: check whether pointed file exists!
    filePath = ''
    if len(sys.argv) < 2:
        filePath = './resources/tone.wav'
    else:
        filePath = sys.argv[1]
    
    audio = readFile(filePath)
    Audio.setFields(audio.getnchannels(), audio.getsampwidth(), audio.getframerate(),
                    audio.getnframes(), audio.getcompname(), audio.getcompname())
    Logger.logAudioInfo(filePath)
    
    return audio


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = App()
    form.show()
    drawOnce(getAudioFile(), form.fileFFTChart)
    # form.update()  # start with something
    app.exec_()
    print("DONE")
