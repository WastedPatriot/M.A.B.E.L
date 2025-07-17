from core.plugin_base import PluginBase
import subprocess

class WifiCrackerPlugin(PluginBase):
    @property
    def name(self): return "WiFi Cracker"
    @property
    def description(self): return "Cracks WPA/WPA2 WiFi networks using aircrack-ng (Linux/WSL required)."

    def run(self, interface="", ssid="", wordlist="", **kwargs):
        if not interface or not ssid or not wordlist:
            return "Usage: interface=<iface> ssid=<ssid> wordlist=<wordlist>"
        try:
            cap_file = "/tmp/handshake.cap"
            # This demo assumes capture is already done (actual attacks require airodump-ng etc.)
            result = subprocess.check_output(
                ["aircrack-ng", "-w", wordlist, "-b", ssid, cap_file],
                universal_newlines=True
            )
            return result
        except Exception as e:
            return f"WiFi cracking failed: {e}"

def get_plugin():
    return WifiCrackerPlugin()
