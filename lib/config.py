import toml

from os import path


def expanded(p):
    return path.expandvars(path.expanduser(p))


class Config:
    def __init__(self, file_name):
        with open(file_name) as file:
            self._config = toml.load(file)

    @property
    def target_dir(self):
        return expanded(self._config["target_dir"])

    @property
    def game_dir(self):
        return path.join(self.target_dir, "KSP_linux")

    @property
    def install_base(self):
        return expanded(self._config["install"]["base"])

    @property
    def install_dlc1(self):
        return expanded(self._config["install"]["dlc1"])

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
        return self._mod_config["source"]

    @property
    def dependencies(self):
        if "depends" in self._mod_config:
            return self._mod_config["depends"]
        return []

    @property
    def checkout(self):
        if "branch" in self._mod_config:
            return self._mod_config["branch"]
        elif "tag" in self._mod_config:
            return self._mod_config["tag"]
        return "master"