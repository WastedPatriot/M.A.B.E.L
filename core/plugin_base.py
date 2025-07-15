# core/plugin_base.py

class PluginBase:
    """
    Abstract base class for all plugins. Enforces properties and methods.
    """
    @property
    def name(self) -> str:
        raise NotImplementedError("Plugin must define a 'name' property.")

    @property
    def description(self) -> str:
        return "No description provided."

    def run(self, **kwargs):
        """
        Main execution logic. Override in your plugin.
        """
        raise NotImplementedError("Plugin must implement a 'run' method.")

    def validate_args(self, **kwargs):
        """
        Optional: validate or sanitize arguments before run().
        """
        pass
