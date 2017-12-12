from src.Observer import Observer
from src.Engine.PluginModule.PluginLoader import PluginLoader
from src.Engine.PluginModule.PluginAbstractModel import PluginAbstractModel
import os

from src.tools.Logger import Logger


def findPluginFiles(packagePath: str = "./plugins"):
    import re
    filesList = os.listdir(packagePath)
    properPluginNames = []
    for fileName in filesList:
        if bool(re.match(".*Plugin.py$", fileName)):
            properPluginNames.append(fileName)
    
    return properPluginNames


class PluginHandler:
    """
    Class observers for new data from Stream, uses loaded pluginns to process/interpret data and Logs(Treminal/UI)
    data(:str) it retrieve from ones.
    """
    def __init__(self):
        self.pluginClassesObjects = []
        # TODO: plugins package paths external config
        import os
        print(os.listdir("./"))
        self.foundPluginFiles = findPluginFiles("./src/Engine/PluginModule/plugins")
        self.pluginResponseDict: {} = {}
        
        for pluginName in self.foundPluginFiles:
            self.pluginClassesObjects.append(PluginLoader.loadPlugin(pluginName))
            self.pluginResponseDict[pluginName] = []

    def handleNewChunk(self, data):
        for p in self.pluginClassesObjects:
            Logger.pluginLog("Not implemented :'(", p.process(data))
            
    def searchForNewPlugins(self):
        raise NotImplementedError()
