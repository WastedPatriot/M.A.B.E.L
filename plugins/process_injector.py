from core.plugin_base import PluginBase
import subprocess

class ProcessInjectorPlugin(PluginBase):
    @property
    def name(self): return "Process Injector"
    @property
    def description(self): return "Injects a payload into a target process using C injector (see c_plugins/process_injector)."

    def run(self, target_pid="", payload="", **kwargs):
        if not target_pid or not payload:
            return "Usage: target_pid=<pid> payload=<shellcode_path>"
        try:
            exe_path = "./c_plugins/process_injector.exe"
            result = subprocess.check_output([exe_path, target_pid, payload], universal_newlines=True)
            return result
        except Exception as e:
            return f"Process injection failed: {e}"

def get_plugin():
    return ProcessInjectorPlugin()
