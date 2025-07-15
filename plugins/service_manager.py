from core.plugin_base import PluginBase
import subprocess

class ServiceManagerPlugin(PluginBase):
    @property
    def name(self):
        return "Service Manager"
    @property
    def description(self):
        return "Start/stop a service by name. Args: action, name"
    def run(self, action="stop", name="", **kwargs):
        if not name:
            return "No service name provided."
        try:
            result = subprocess.check_output(
                ["sc", action, name], text=True
            )
            return f"Service {name} {action}ed:\n{result}"
        except Exception as e:
            return f"Service {action} {name} failed: {e}"

def get_plugin():
    return ServiceManagerPlugin()
