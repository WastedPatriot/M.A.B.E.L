from core.plugin_base import PluginBase
import subprocess

class RemoteCodeExecPlugin(PluginBase):
    @property
    def name(self): return "Remote Code Exec"
    @property
    def description(self): return "Executes arbitrary code on remote or local machine (simulated here)."

    def run(self, cmd="", target="local", **kwargs):
        if not cmd:
            return "Usage: cmd=<command>"
        try:
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            return output
        except Exception as e:
            return f"Remote code execution failed: {e}"

def get_plugin():
    return RemoteCodeExecPlugin()
