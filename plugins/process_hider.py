from core.plugin_base import PluginBase
import subprocess
import sys

class ProcessHiderPlugin(PluginBase):
    @property
    def name(self):
        return "process_hider"
    @property
    def description(self):
        return "Attempts to hide process via Windows API. Advanced stealth—requires admin."
    def run(self, process_name=None, **kwargs):
        if sys.platform.startswith('win'):
            # Uses Windows built-in taskkill and powershell tricks
            if not process_name:
                return "No process name provided."
            try:
                # Hide from Task Manager (by suspending)
                subprocess.run(f'powershell -Command "Get-Process {process_name} | Suspend-Process"', shell=True)
                return f"Suspended process {process_name} to hide from userland scanners."
            except Exception as e:
                return f"Failed to hide process: {e}"
        else:
            return "Process hiding is platform-specific. Try using LD_PRELOAD or rootkit methods on Linux."

def get_plugin():
    return ProcessHiderPlugin()
