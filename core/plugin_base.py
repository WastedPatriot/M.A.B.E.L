class PluginBase:
    @property
    def name(self):
        raise NotImplementedError
    @property
    def description(self):
        return "No description provided."
    def run(self, **kwargs):
        raise NotImplementedError
