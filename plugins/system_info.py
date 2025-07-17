from core.plugin_base import PluginBase
import platform
import psutil

class SystemInfoPlugin(PluginBase):
    @property
    def name(self): return "System Info"
    @property
    def description(self): return "Displays hardware, OS, CPU, RAM, and disk stats."

    def run(self, **kwargs):
        try:
            info = [
                f"Hostname: {platform.node()}", # Hostname of the machine
                f"OS: {platform.system()} {platform.release()}", # Operating System and its release version
                f"CPU: {platform.processor()}", # Processor information
                f"RAM: {psutil.virtual_memory().total // (1024 ** 2)} MB", # Total RAM in MB
                f"Disk: {psutil.disk_usage('/').total // (1024 ** 3)} GB" # Total disk space of the root partition in GB
            ]
            return "\n".join(info)
        except Exception as e:
            return f"System info failed: {e}"

def get_plugin():
    return SystemInfoPlugin()