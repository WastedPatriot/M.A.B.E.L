import os

template = '''
from core.plugin_base import PluginBase

class {ClassName}(PluginBase):
    @property
    def name(self):
        return "{PluginName}"

    @property
    def description(self):
        return "{Description}"

    def run(self, {Args}**kwargs):
        # TODO: Implement your plugin logic here
        return "{PluginName} plugin executed. (Implement logic!)"

def get_plugin():
    return {ClassName}()
'''

def to_class_name(name):
    return ''.join(part.capitalize() for part in name.split('_')) + 'Plugin'

def main():
    print("Plugin generator for your AI hacking toolkit.")
    fname = input("Plugin file name (no .py): ").strip()
    plugin_name = input("Plugin display name: ").strip()
    description = input("Short description: ").strip()
    args = input("Args (comma separated, leave blank if none): ").strip()
    args_str = ', '.join([f"{arg}=''" for arg in args.split(',') if arg.strip()])
    if args_str:
        args_str += ', '

    class_name = to_class_name(fname)
    code = template.format(
        ClassName=class_name,
        PluginName=plugin_name,
        Description=description,
        Args=args_str
    )

    out_file = os.path.join("plugins", f"{fname}.py")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Created plugin: plugins/{fname}.py")

if __name__ == "__main__":
    main()
