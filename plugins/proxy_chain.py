from core.plugin_base import PluginBase
import subprocess
import shutil
import sys

class ProxyChainPlugin(PluginBase):
    @property
    def name(self):
        return "proxy_chain"
    @property
    def description(self):
        return "Runs any command via proxychains. Args: cmd"
    def run(self, cmd=None, **kwargs):
        if sys.platform.startswith('linux'):
            if shutil.which("proxychains") is None:
                subprocess.run("sudo apt install -y proxychains", shell=True)
            if not cmd:
                return "No command provided to run via proxychains."
            proc = subprocess.Popen(f"proxychains {cmd}", shell=True)
            return f"Started '{cmd}' through proxychains as process {proc.pid}."
        else:
            return "Proxychains is not natively supported on Windows. Use VPN/Tor plugins."

def get_plugin():
    return ProxyChainPlugin()
