# core/plugins.py

import os
import sys
import importlib
import logging

PLUGIN_FOLDER = "plugins"

def discover_plugins() -> list:
    """
    Dynamically discover and load all plugins in the plugins/ folder.
    Supports hot reload for rapid development.
    """
    plugins = []
    sys.path.insert(0, PLUGIN_FOLDER)  # Temporarily add plugin dir to sys.path
    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and not filename.startswith("_"):
            modulename = filename[:-3]
            try:
                # Hot reload if module is already loaded
                if modulename in sys.modules:
                    module = importlib.reload(sys.modules[modulename])
                else:
                    module = importlib.import_module(modulename)
                if hasattr(module, "get_plugin"):
                    plugin = module.get_plugin()
                    plugins.append(plugin)
            except Exception as e:
                logging.error(f"[PLUGIN LOAD ERROR] {modulename}: {e}")
    sys.path.pop(0)
    return plugins

def get_plugin_by_name(name: str):
    """
    Retrieve a plugin by its name (case-insensitive).
    """
    for plugin in discover_plugins():
        if plugin.name.lower() == name.lower():
            return plugin
    return None

def reload_plugins():
    """
    Utility for explicit reload; returns new plugin list.
    """
    return discover_plugins()
