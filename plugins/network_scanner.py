from core.plugin_base import PluginBase
import subprocess

class NetworkScannerPlugin(PluginBase):
    @property
    def name(self): return "Network Scanner"
    @property
    def description(self): return "Scans a target IP or subnet for open ports and services using Nmap."

    def run(self, target="127.0.0.1", **kwargs):
        try:
            cmd = ["nmap", "-T4", "-A", target]
            result = subprocess.check_output(cmd, universal_newlines=True)
            return result
        except Exception as e:
            return f"Network scan failed: {e}"

def get_plugin():
    return NetworkScannerPlugin()
