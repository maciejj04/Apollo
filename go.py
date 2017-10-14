import os
import sys

from PyQt4 import QtGui

from src.Commons.Audio import Audio
from src.Commons.CommonAudioInfo import CommonAudioInfo as Cai
from src.Engine.ReadFile import readFile
from src.UI.App import App
from src.UI.drawOnce import drawOnce
from src.tools.Logger import Logger


def getInputArguments():
    return './resources/pra.wav' if len(sys.argv) < 2 else sys.argv[1]


def validateFilePath(filePath):
    if not os.path.exists(filePath):
        Logger.info("Path to file does not exist! [{filepath}]".format(filepath=filePath))
        raise ValueError("Path to file does not exist! [{filepath}]".format(filepath=filePath))
    
    return True


def getAudioFile():
    
    filePath = getInputArguments()
    validateFilePath(filePath)

    audio = readFile(filePath)
    Audio.setFields(filePath, audio.getnchannels(), audio.getsampwidth(), audio.getframerate(),
                    audio.getnframes(), audio.getcompname(), audio.getcompname())
    Cai.numberOfFrames = audio.getnframes()

    Logger.logAudioInfo()

    return audio


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = App()
    form.show()
    drawOnce(getAudioFile(), form.fileFFTChart)
    form.update()  # start with something
    app.exec_()
    print("DONE")
