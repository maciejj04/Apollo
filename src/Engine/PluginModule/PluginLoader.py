from src.tools.Logger import Logger


class PluginLoader:
    loadedModulesClasses: [] = []
    
    @classmethod
    def loadPlugin(cls, name):
        """
        :param name: module file name
        :return: loaded module class object.
        """
        name = name[:-3]  # TODO: workaround for now to cut file Extension :P
        try:
            # TODO: validate if fetched class implements PluginAbstractModel
            import importlib
            module = importlib.import_module("plugins."+name)
            moduleClass = getattr(module, name)
            if moduleClass in cls.loadedModulesClasses:
                Logger.warninig("Module already loaded!")
                return

            cls.loadedModulesClasses.append(moduleClass)
            
            Logger.info("Dynamically loaded plugin :" + name)
            return moduleClass()
        
        except ValueError as e:  # Exception?
            print("No Model named: " + name)
            raise e
