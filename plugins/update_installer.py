from core.plugin_base import PluginBase
import subprocess

class UpdateInstallerPlugin(PluginBase):
    @property
    def name(self):
        return "Update Installer"
    @property
    def description(self):
        return "Checks and installs Windows Updates. No args."
    def run(self, **kwargs):
        try:
            result = subprocess.check_output(
                ["powershell", "-Command", "Install-WindowsUpdate -AcceptAll -AutoReboot"], text=True
            )
            return f"Update result:\n{result}"
        except Exception as e:
            return f"Update failed: {e}"

def get_plugin():
    return UpdateInstallerPlugin()
