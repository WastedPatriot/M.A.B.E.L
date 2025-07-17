from core.plugin_base import PluginBase
import subprocess

class FixNetworkPlugin(PluginBase):
    @property
    def name(self): return "Fix Network"
    @property
    def description(self): return "Diagnoses and repairs network connectivity issues."

    def run(self, target="local", **kwargs):
        try:
            # Flush DNS and reset network adapters (Windows)
            subprocess.call("ipconfig /flushdns", shell=True)
            subprocess.call("netsh winsock reset", shell=True)
            subprocess.call("netsh int ip reset", shell=True)
            return "Network stack reset and DNS flushed."
        except Exception as e:
            return f"Network repair failed: {e}"

def get_plugin():
    return FixNetworkPlugin()
