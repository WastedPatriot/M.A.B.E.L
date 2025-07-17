from core.plugin_base import PluginBase
import subprocess

class UpdateInstallerPlugin(PluginBase):
    @property
    def name(self): return "Update Installer"
    @property
    def description(self): return "Checks for and installs system updates (Windows only, demo)."

    def run(self, action="check", **kwargs):
        try:
            if action == "check":
                cmd = ["powershell", "-Command", "Get-WindowsUpdate"]
            elif action == "install":
                cmd = ["powershell", "-Command", "Install-WindowsUpdate -AcceptAll -AutoReboot"]
            else:
                return f"Unknown update action: {action}"
            output = subprocess.check_output(cmd, universal_newlines=True)
            return output
        except Exception as e:
            return f"Update installer failed: {e}"

def get_plugin():
    return UpdateInstallerPlugin()
