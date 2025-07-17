from core.plugin_base import PluginBase
import os
import shutil

class DiskCleanerPlugin(PluginBase):
    @property
    def name(self): return "Disk Cleaner"
    @property
    def description(self): return "Deletes temporary files and frees disk space."

    def run(self, target="local", **kwargs):
        try:
            count = 0
            temp_dir = os.getenv('TEMP') or '/tmp'
            for root, dirs, files in os.walk(temp_dir):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                        count += 1
                    except Exception:
                        pass
            return f"Deleted {count} temp files from {temp_dir}."
        except Exception as e:
            return f"Disk cleaner failed: {e}"

def get_plugin():
    return DiskCleanerPlugin()
