from core.plugin_base import PluginBase
import os

class PluginCreatorPlugin(PluginBase):
    @property
    def name(self): return "Plugin Creator"
    @property
    def description(self): return "Creates a new Python plugin from code (admin required)."

    def run(self, plugin_name="", code="", **kwargs):
        if not plugin_name or not code:
            return "Usage: plugin_name=<name> code=<python_code>"
        fname = plugin_name.lower() + ".py"
        path = os.path.join("plugins", fname)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            return f"Plugin '{plugin_name}' created at {path}."
        except Exception as e:
            return f"Plugin creation failed: {e}"

def get_plugin():
    return PluginCreatorPlugin()
