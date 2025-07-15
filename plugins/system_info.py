from core.plugin_base import PluginBase
import platform

class SystemInfoPlugin(PluginBase):
    @property
    def name(self):
        return "System Info"

    @property
    def description(self):
        return "Displays OS, Python version, and basic machine info."

    def run(self, **kwargs):
        info = (
            f"OS: {platform.system()} {platform.release()}\n"
            f"Python: {platform.python_version()}\n"
            f"Machine: {platform.machine()}\n"
            f"Processor: {platform.processor()}\n"
        )
        return info

def get_plugin():
    return SystemInfoPlugin()
