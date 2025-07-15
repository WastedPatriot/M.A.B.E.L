from core.plugin_base import PluginBase
import subprocess

class FixNetworkPlugin(PluginBase):
    @property
    def name(self):
        return "Fix Network"
    @property
    def description(self):
        return "Repairs Windows network stack (flush DNS, reset adapter). No args."
    def run(self, **kwargs):
        cmds = [
            ["ipconfig", "/flushdns"],
            ["netsh", "int", "ip", "reset"],
            ["netsh", "winsock", "reset"]
        ]
        out = ""
        for cmd in cmds:
            try:
                result = subprocess.check_output(cmd, text=True)
                out += f"{' '.join(cmd)}:\n{result}\n"
            except Exception as e:
                out += f"{' '.join(cmd)} failed: {e}\n"
        return out

def get_plugin():
    return FixNetworkPlugin()
