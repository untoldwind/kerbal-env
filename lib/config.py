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

