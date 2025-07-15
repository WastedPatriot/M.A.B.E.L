from core.plugin_base import PluginBase
import subprocess

class DiskCleanerPlugin(PluginBase):
    @property
    def name(self):
        return "Disk Cleaner"
    @property
    def description(self):
        return "Runs Windows Disk Cleanup (cleanmgr). No args."
    def run(self, **kwargs):
        try:
            result = subprocess.check_output(
                ["cleanmgr", "/sagerun:1"], text=True
            )
            return f"Disk cleanup started:\n{result}"
        except Exception as e:
            return f"Disk cleanup failed: {e}"

def get_plugin():
    return DiskCleanerPlugin()
