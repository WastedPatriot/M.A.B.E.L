from core.plugin_base import PluginBase
import subprocess

class EventLogParserPlugin(PluginBase):
    @property
    def name(self):
        return "Event Log Parser"
    @property
    def description(self):
        return "Shows last 10 System event log entries. No args."
    def run(self, **kwargs):
        try:
            result = subprocess.check_output(
                ["wevtutil", "qe", "System", "/c:10", "/f:text"], text=True
            )
            return f"Last 10 System event log entries:\n{result}"
        except Exception as e:
            return f"Event log parse failed: {e}"

def get_plugin():
    return EventLogParserPlugin()
