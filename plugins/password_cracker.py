from core.plugin_base import PluginBase
import subprocess

class PasswordCrackerPlugin(PluginBase):
    @property
    def name(self): return "Password Cracker"
    @property
    def description(self): return "Attempts to crack password hashes using hashcat."

    def run(self, hashfile="", mode="0", wordlist="", **kwargs):
        if not hashfile or not wordlist:
            return "Usage: hashfile=<file> mode=<hashcat_mode> wordlist=<file>"
        try:
            cmd = [
                "hashcat", "-m", str(mode), hashfile, wordlist, "--force", "--potfile-disable"
            ]
            result = subprocess.check_output(cmd, universal_newlines=True)
            return result
        except Exception as e:
            return f"Password crack failed: {e}"

def get_plugin():
    return PasswordCrackerPlugin()
