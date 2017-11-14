# TODO:
import abc
from functools import wraps

from .Observer import Observer
import threading


def executeInNewThread(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        import random
        func_hl = threading.Thread(name="notify_thread:{}".format(random.randint(0, 9999)), target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl
    
    return async_func


class Observable(abc.ABC):
    def __init__(self):
        self._observers: list = []
    
    @property
    def getObservers(self) -> [Observer]:
        return self._observers
    
    def addObserver(self, o: Observer):
        self._observers.append(o)
    
    def deleteObserver(self, o: Observer):
        self._observers.remove(o)
    
    @abc.abstractmethod
    def notifyObservers(self, data):
        return
