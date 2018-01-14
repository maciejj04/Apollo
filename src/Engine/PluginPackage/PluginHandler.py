from Commons import Settings
from Commons.Settings import ENABLE_PLUGINS
from src.MessageServer import MessageServer, MsgTypes
from src.Observer import Observer
from src.Engine.PluginPackage.PluginLoader import PluginLoader
from src.Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel
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
        if not Settings.ENABLE_PLUGINS:
            Logger.info("Plugins DISABLED!")
            
        self.pluginClassesObjects = []
        # TODO: plugins package paths external config
        import os
        print(os.listdir("./"))
        self.foundPluginFiles = findPluginFiles("./src/Engine/PluginPackage/plugins")
        self.pluginResponseDict: {} = {}
        
        for pluginName in self.foundPluginFiles:
            pluginClassObj = PluginLoader.loadPlugin(pluginName)
            if type(pluginClassObj).__name__ == "StaticCorrPlugin":                         # Little hack for now :'D
                MessageServer.registerForEvent(pluginClassObj, MsgTypes.RECORDING_STOP)
                
            self.pluginClassesObjects.append(pluginClassObj)
            self.pluginResponseDict[pluginName] = []
    
    def handleNewChunk(self, data):
        if not ENABLE_PLUGINS:
            return
        for p in self.pluginClassesObjects:
            Logger.pluginLog("x ", p.process(data))
    
    def searchForNewPlugins(self):
        raise NotImplementedError()
        
        
        # TODO: update settings as windowWidth for plugins etc. when triggeered from UI settings.
