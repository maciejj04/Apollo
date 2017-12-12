from src.Engine.PluginModule.PluginAbstractModel import PluginAbstractModel


class CorrPlugin(PluginAbstractModel):
    
    def process(self, data) -> str:
        return "CorrPlugin handled data"
