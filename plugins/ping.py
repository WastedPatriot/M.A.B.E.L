from core.plugin_base import PluginBase
import subprocess

class PingPlugin(PluginBase):
    @property
    def name(self): return "Ping"
    @property
    def description(self): return "Pings a target host to test reachability."

    def run(self, target="8.8.8.8", count="4", **kwargs):
        try:
            cmd = ["ping", target, "-n", str(count)]
            result = subprocess.check_output(cmd, universal_newlines=True)
            return result
        except Exception as e:
            return f"Ping failed: {e}"

def get_plugin():
    return PingPlugin()
