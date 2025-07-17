import os
import sys
import importlib

PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'plugins')
PLUGIN_FOLDER = os.path.abspath(PLUGIN_FOLDER)

def discover_plugins():
    plugins = []
    sys.path.insert(0, PLUGIN_FOLDER)
    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".py") and not filename.startswith("_"):
            modulename = filename[:-3]
            try:
                if modulename in sys.modules:
                    module = importlib.reload(sys.modules[modulename])
                else:
                    module = importlib.import_module(modulename)
                if hasattr(module, "get_plugin"):
                    plugin = module.get_plugin()
                    plugins.append(plugin)
            except Exception as e:
                print(f"Plugin load error ({modulename}): {e}")
    sys.path.pop(0)
    return plugins

def get_plugin_by_name(name):
    for plugin in discover_plugins():
        if plugin.name.lower() == name.lower():
            return plugin
    return None

def reload_plugins():
    return discover_plugins()
def get_plugin_by_name_dynamic(name):
    """
    Dynamically loads and returns a plugin by its name.
    This is useful for cases where the plugin might have been created
    after the initial discover_plugins call.
    """
    safe_name = "".join(c for c in name if c.isalnum() or c == "_").lower()
    modulename = safe_name
    try:
        if modulename in sys.modules:
            module = importlib.reload(sys.modules[modulename])
        else:
            # Add plugin folder to path if not already there
            if PLUGIN_FOLDER not in sys.path:
                sys.path.insert(0, PLUGIN_FOLDER)
            module = importlib.import_module(modulename)
            if PLUGIN_FOLDER in sys.path:
                sys.path.remove(PLUGIN_FOLDER) # Clean up sys.path
        if hasattr(module, "get_plugin"):
            return module.get_plugin()
    except Exception as e:
        print(f"Dynamic plugin load error ({modulename}): {e}")
    return None
