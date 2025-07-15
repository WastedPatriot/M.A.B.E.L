from core.plugin_base import PluginBase
import subprocess

class ProcessKillerPlugin(PluginBase):
    @property
    def name(self):
        return "Process Killer"
    @property
    def description(self):
        return "Kill a process by name. Args: name"
    def run(self, name="", **kwargs):
        if not name:
            return "No process name provided."
        try:
            result = subprocess.check_output(
                ["taskkill", "/im", name, "/f"], text=True
            )
            return f"Process {name} killed:\n{result}"
        except Exception as e:
            return f"Killing process {name} failed: {e}"

def get_plugin():
    return ProcessKillerPlugin()
