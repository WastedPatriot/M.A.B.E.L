from core.plugin_base import PluginBase
import subprocess

class EventLogParserPlugin(PluginBase):
    @property
    def name(self): return "Event Log Parser"
    @property
    def description(self): return "Parses Windows Event Logs for suspicious activity."

    def run(self, log="System", **kwargs):
        try:
            # On Windows, use 'wevtutil' to query logs
            output = subprocess.check_output(
                ["wevtutil", "qe", log, "/c:10", "/f:text"], universal_newlines=True
            )
            return f"Last 10 events from {log}:\n{output}"
        except Exception as e:
            return f"Event log parsing failed: {e}"

def get_plugin():
    return EventLogParserPlugin()
