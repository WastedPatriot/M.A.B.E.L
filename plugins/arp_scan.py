from core.plugin_base import PluginBase
import subprocess

class ARPScanPlugin(PluginBase):
    @property
    def name(self):
        return "ARP Scan"
    @property
    def description(self):
        return "Scan LAN for live hosts using arp. Args: network"
    def run(self, network="192.168.1.0/24", **kwargs):
        try:
            result = subprocess.check_output(
                ["arp", "-a"], text=True
            )
            return f"ARP scan result:\n{result}"
        except Exception as e:
            return f"ARP scan failed: {e}"

def get_plugin():
    return ARPScanPlugin()
