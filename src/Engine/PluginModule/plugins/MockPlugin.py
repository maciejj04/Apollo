from src.Engine.PluginModule.PluginAbstractModel import PluginAbstractModel


class MockPlugin(PluginAbstractModel):
    def process(self, data) -> str:
        return "MockPlugin There I am!"
