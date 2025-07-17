from core.plugin_base import PluginBase
import subprocess
import sys
import os

class TorTunnelPlugin(PluginBase):
    @property
    def name(self): return "tor_tunnel"
    @property
    def description(self): return "Starts Tor SOCKS5 proxy and optionally routes system/browser/hacking traffic through it."

    def run(self, **kwargs):
        # Install tor if missing (Windows: choco, Linux: apt)
        if sys.platform.startswith('win'):
            subprocess.run("choco install -y tor", shell=True)
        elif sys.platform.startswith('linux'):
            subprocess.run("sudo apt install -y tor", shell=True)
        # Start tor in background (default SOCKS5 on 127.0.0.1:9050)
        proc = subprocess.Popen(["tor"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # (Optional) Set system env or tell user to use 127.0.0.1:9050 for SOCKS5
        os.environ["ALL_PROXY"] = "socks5://127.0.0.1:9050"
        return f"Tor proxy launched (SOCKS5 127.0.0.1:9050) as PID {proc.pid}. Set ALL_PROXY or use proxychains."

def get_plugin(): return TorTunnelPlugin()
