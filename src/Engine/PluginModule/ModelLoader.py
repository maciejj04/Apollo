from src.tools.Logger import Logger


class ModelLoader:
    def __init__(self):
        foundModules: [] = []
    
    def loadModule(self, name):
        try:
            # TODO check if already loaded
            module = __import__(name, globals(), locals(), [name], -1)
            moduleClass = getattr(module, name)
            
            Logger.info("Dynamically loaded model :" + name)
            classObj = moduleClass()
            return classObj
        except Exception as e:
            print("No Model named: " + name + ", Error : " + e.message)
            raise e
