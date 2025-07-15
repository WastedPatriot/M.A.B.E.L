# plugins/plugin_creator.py

from core.plugin_base import PluginBase
import os

class PluginCreator(PluginBase):
    @property
    def name(self):
        return "Plugin Creator"
    @property
    def description(self):
        return "Creates and installs a new plugin from provided Python code."

    def run(self, plugin_name, code, **kwargs):
        # Sanitize plugin_name for file safety
        safe_name = "".join(c for c in plugin_name if c.isalnum() or c == "_").lower()
        file_path = os.path.join("plugins", f"{safe_name}.py")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            return f"Plugin '{plugin_name}' successfully written to {file_path}."
        except Exception as e:
            return f"Failed to create plugin: {e}"

def get_plugin():
    return PluginCreator()
