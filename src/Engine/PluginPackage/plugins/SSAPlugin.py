from src.Engine.PluginPackage.PluginAbstractModel import PluginAbstractModel


class SSAPlugin(PluginAbstractModel):
    def process(self, data) -> str:
        return "SSAPlugin there i am!"
