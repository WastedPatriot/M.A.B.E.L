from core.plugin_base import PluginBase
import platform
import datetime

class ReportGeneratorPlugin(PluginBase):
    @property
    def name(self): return "Report Generator"
    @property
    def description(self): return "Creates a summary report of host info, recent activity, and notable findings."

    def run(self, **kwargs):
        info = [
            f"=== M.A.B.E.L Host Report ===",
            f"Generated: {datetime.datetime.now()}",
            f"OS: {platform.system()} {platform.release()}",
            f"Node: {platform.node()}",
            f"Arch: {platform.machine()}",
            f"Python: {platform.python_version()}",
            "",
            "Custom findings and activity logs could be added here."
        ]
        return "\n".join(info)

def get_plugin():
    return ReportGeneratorPlugin()
