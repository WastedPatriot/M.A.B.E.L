from core.plugin_base import PluginBase
import subprocess

class ServiceManagerPlugin(PluginBase):
    @property
    def name(self): return "Service Manager"
    @property
    def description(self): return "Manages Windows services (start, stop, query)."

    def run(self, action="query", service="", **kwargs):
        try:
            if action == "query":
                cmd = ["sc", "query", service] if service else ["sc", "query"]
            elif action == "start":
                cmd = ["sc", "start", service]
            elif action == "stop":
                cmd = ["sc", "stop", service]
            else:
                return f"Unknown action: {action}"
            result = subprocess.check_output(cmd, universal_newlines=True)
            return result
        except Exception as e:
            return f"Service manager failed: {e}"

def get_plugin():
    return ServiceManagerPlugin()
