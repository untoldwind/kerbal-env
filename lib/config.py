import toml

from string import Template
import pathlib

def merge(source, dest):
    for key, value in source.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            merge(value, node)
        else:
            dest[key] = value
    return dest

class Config:
    def __init__(self, file_name):
        with open(file_name) as file:
            self._config = toml.load(file)
        if "include" in self._config:
            for file_name in self._config["include"]:
                self._config = merge(self._config, toml.load(file_name))

    @property
    def target_dir(self):
        return pathlib.Path(self._config["target_dir"]).expanduser()

    @property
    def game_dir(self):
        return self.target_dir.joinpath("KSP_linux")

    @property
    def install_base(self):
        return pathlib.Path(self._config["install"]["base"]).expanduser()

    @property
    def has_dlc1(self):
        return "dlc1" in self._config["install"]
        
    @property
    def install_dlc1(self):
        return pathlib.Path(self._config["install"]["dlc1"]).expanduser()

    @property
    def mods(self):
        return {name: ModConfig(self.game_dir, mod_config) for name, mod_config in self._config["mods"].items()}

    def dump(self):
        return toml.dumps(self._config)

class ModConfig:
    def __init__(self, game_dir, mod_config):
        self.game_dir = game_dir
        self._mod_config = mod_config

    @property
    def enabled(self):
        if "enabled" in self._mod_config:
            return self._mod_config["enabled"]
        return True

    @property
    def source_type(self):
        return self._mod_config["source_type"]

    @property
    def source(self):
        if "source" in self._mod_config:
            source_raw = self._mod_config["source"]
            template = Template(source_raw)
            return template.substitute(version=self.version)
        return None

    @property
    def version(self):
        if "version" in self._mod_config:
            return self._mod_config["version"]
        return "unknown"

    @property
    def patch(self):
        if "patch" in self._mod_config:
            return self._mod_config["patch"]
        return None

    @property
    def checkout_is_tag(self):
        return "tag" in self._mod_config

    @property
    def checkout(self):
        if "branch" in self._mod_config:
            return self._mod_config["branch"]
        elif "tag" in self._mod_config:
            return self._mod_config["tag"]
        return "master"