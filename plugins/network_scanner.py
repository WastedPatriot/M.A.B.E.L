from core.plugin_base import PluginBase
import subprocess

class NetworkScannerPlugin(PluginBase):
    @property
    def name(self):
        return "Network Scanner"

    @property
    def description(self):
        return "Scans a target IP or subnet using nmap. Args: target or ip"

    def run(self, target="127.0.0.1", ip=None, **kwargs):
        # Accept either 'target' or 'ip' as argument for compatibility with AI
        scan_target = ip if ip is not None else target
        nmap_path = "nmap"  # Or full path if needed
        try:
            result = subprocess.run(
                [nmap_path, "-T4", "-F", scan_target],
                capture_output=True,
                text=True,
                timeout=30   # Prevent hanging
            )
            if result.returncode == 0:
                return f"Scan result for {scan_target}:\n{result.stdout}"
            else:
                return f"Scan failed (code {result.returncode}):\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Scan timed out after 30 seconds."
        except Exception as e:
            return f"Scan failed: {e}"

def get_plugin():
    return NetworkScannerPlugin()
