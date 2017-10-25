#TODO:


class Observable():
    _observers: list = []
    
    def addObserver(self, o):
        self._observers.append(o)
        
    def notifyObservers(self, data):
        pass