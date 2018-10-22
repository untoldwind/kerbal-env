import toml

from string import Template
import pathlib


class Config:
    def __init__(self, file_name):
        with open(file_name) as file:
            self._config = toml.load(file)

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
    def install_dlc1(self):
        return pathlib.Path(self._config["install"]["dlc1"]).expanduser()

    @property
    def mods(self):
        return {name: ModConfig(self.game_dir, mod_config) for name, mod_config in self._config["mods"].items()}


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
    def dependencies(self):
        if "depends" in self._mod_config:
            return self._mod_config["depends"]
        return []

    @property
    def patch(self):
        if "patch" in self._mod_config:
            return self._mod_config["patch"]
        return None

    @property
    def checkout(self):
        if "branch" in self._mod_config:
            return self._mod_config["branch"]
        elif "tag" in self._mod_config:
            return self._mod_config["tag"]
        return "master"