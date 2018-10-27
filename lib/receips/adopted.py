import shutil
import pathlib
from lib.utils import rm_rf


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir

    def build(self):
        pass

    def install(self):
        adopted_path = pathlib.Path().joinpath("adopted").resolve()
        target_dir = self.game_dir.joinpath("GameData", "XyphosAerospace")
        rm_rf(target_dir)
        shutil.copytree(adopted_path.joinpath(
            "GameData", "XyphosAerospace"), target_dir)

    def check_installed(self):
        target_dir = self.game_dir.joinpath("GameData", "XyphosAerospace")
        return target_dir.exists()
