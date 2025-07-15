from core.plugin_base import PluginBase
import datetime

class ReportGeneratorPlugin(PluginBase):
    @property
    def name(self):
        return "Report Generator"
    @property
    def description(self):
        return "Generates a basic report with date/time. No args."
    def run(self, **kwargs):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Report generated at {now}.\n(Add your report content here.)"

def get_plugin():
    return ReportGeneratorPlugin()
