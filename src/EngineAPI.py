
from PyQt4 import QtCore

class EngineAPI(QtCore.QThread):
    
    @classmethod
    def notifyFFTChart(cls):
        QtCore.QThread.__init__(cls)
        cls.signal = QtCore.SIGNAL("signal")