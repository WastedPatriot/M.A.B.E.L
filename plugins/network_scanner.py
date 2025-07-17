import subprocess
import socket

class NetworkScannerPlugin:
    @property
    def name(self):
        return "Network Scanner"
    @property
    def description(self):
        return "Scans a target IP or hostname using nmap. Args: target"
    def run(self, target, **kwargs):
        # Try to resolve domain to IP (if it's not already an IP)
        try:
            ip = socket.gethostbyname(target)
        except Exception:
            ip = target  # Use as-is if not resolvable
        cmd = f"nmap -Pn {ip}"
        result = subprocess.getoutput(cmd)
        return f"Scan result for {target}:\n{result}"

def get_plugin():
    return NetworkScannerPlugin()
