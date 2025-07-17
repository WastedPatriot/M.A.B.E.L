from core.plugin_base import PluginBase
import socket

class WormSpreaderPlugin(PluginBase):
    @property
    def name(self): return "Worm Spreader"
    @property
    def description(self): return "Attempts to propagate to other machines on LAN via open SMB shares (simulated)."

    def run(self, target_subnet="192.168.1.", **kwargs):
        # Simulated scan and copy logic
        found = []
        for host in range(2, 10):
            ip = f"{target_subnet}{host}"
            try:
                s = socket.socket()
                s.settimeout(0.5)
                s.connect((ip, 445))
                found.append(ip)
                s.close()
            except:
                continue
        if not found:
            return "No accessible SMB hosts found for worm propagation."
        return f"Worm propagated to: {', '.join(found)} (simulated, real code would copy payloads here)"

def get_plugin():
    return WormSpreaderPlugin()
