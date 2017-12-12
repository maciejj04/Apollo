import abc


class ModelAbstract(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        print("Model abstract")
    
    @abc.abstractmethod
    def process(self, no_of_elements=1):
        pass
    
    @abc.abstractmethod
    def interpret(self, no_of_elements=1):
        pass