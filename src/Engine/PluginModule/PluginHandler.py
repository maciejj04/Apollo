from src.Observer import Observer
from src.Engine.PluginModule.PluginLoader import PluginLoader
from src.Engine.PluginModule.PluginAbstractModel import PluginAbstractModel
import os


def findPluginFiles(packagePath: str = "./plugins"):
    import re
    filesList = os.listdir(packagePath)
    properPluginNames = []
    for fileName in filesList:
        if bool(re.match(".*Plugin.py$", fileName)):
            properPluginNames.append(fileName)
    
    return properPluginNames


class PluginHandler(Observer):
    """
    Class observers for new data from Stream, uses loaded pluginns to process/interpret data and Logs(Treminal/UI)
    data(:str) it retrieve from ones.
    """
    
    def handleNewData(self, data):
        for p in self.pluginClassesObjects:
            p.process(data)
    
    def __init__(self):
        self.pluginClassesObjects = []
        # TODO: plugins package paths external config
        self.foundPluginFiles = findPluginFiles("./plugins")
        self.pluginResponseDict: {} = {}
        
        for pluginName in self.foundPluginFiles:
            self.pluginClassesObjects.append(PluginLoader.loadPlugin(pluginName))
            self.pluginResponseDict[pluginName] = []


if __name__ == "__main__":
    ph = PluginHandler()
    for e in ph.pluginClassesObjects:
        print(e.process("mock"))