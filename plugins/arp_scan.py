from core.plugin_base import PluginBase
import subprocess

class ArpScanPlugin(PluginBase):
    @property
    def name(self): return "ARP Scan"
    @property
    def description(self): return "Performs ARP scan to discover devices in local network."

    def run(self, target="192.168.1.0/24", **kwargs):
        try:
            result = subprocess.check_output(["arp", "-a"], universal_newlines=True)
            return result
        except Exception as e:
            return f"ARP scan failed: {e}"

def get_plugin():
    return ArpScanPlugin()
