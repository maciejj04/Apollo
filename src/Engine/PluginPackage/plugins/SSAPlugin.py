from src.Engine.PluginModule.PluginAbstractModel import PluginAbstractModel


class SSAPlugin(PluginAbstractModel):
    def process(self, data) -> str:
        return "SSAPlugin there i am!"
