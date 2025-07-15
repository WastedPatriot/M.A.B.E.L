from core.plugin_base import PluginBase
import subprocess

class PingPlugin(PluginBase):
    @property
    def name(self):
        return "Ping"
    @property
    def description(self):
        return "Ping a target IP or hostname. Args: target, count"
    def run(self, target="8.8.8.8", count="4", **kwargs):
        try:
            result = subprocess.check_output(
                ["ping", "-n", str(count), target], text=True
            )
            return f"Ping result for {target}:\n{result}"
        except Exception as e:
            return f"Ping failed: {e}"

def get_plugin():
    return PingPlugin()
