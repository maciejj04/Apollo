# TODO:
import abc
from functools import wraps

from .Observer import Observer
import threading


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
