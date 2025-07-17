from core.plugin_base import PluginBase
import subprocess

class ProcessKillerPlugin(PluginBase):
    @property
    def name(self): return "Process Killer"
    @property
    def description(self): return "Kills a running process by name or PID."

    def run(self, name_or_pid="", **kwargs):
        if not name_or_pid:
            return "Usage: name_or_pid=<name_or_pid>"
        try:
            try:
                pid = int(name_or_pid)
                subprocess.check_output(["taskkill", "/PID", str(pid), "/F"])
            except ValueError:
                subprocess.check_output(["taskkill", "/IM", name_or_pid, "/F"])
            return f"Killed {name_or_pid}."
        except Exception as e:
            return f"Process kill failed: {e}"

def get_plugin():
    return ProcessKillerPlugin()
