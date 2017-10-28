import sys

from PyQt4 import QtGui
from src.UI.App import App

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    ParentWindow = App()
    ParentWindow.show()
    app.exec_()
    print("DONE")
