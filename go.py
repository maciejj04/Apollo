import sys

from PyQt4 import QtGui
from src.UI.App import App
from src.UI.drawOnce import drawOnce
from src.tools.helper_functions import getAudioFile


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ParentWindow = App()
    ParentWindow.show()
    drawOnce(getAudioFile(), ParentWindow.fileFFTChart)
    app.exec_()
    print("DONE")
