import shutil
import pathlib
from lib.utils import rm_rf
from lib.recipes import Receipt


class adopted(Receipt):
    depends=["KOS"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        adopted_path = pathlib.Path().joinpath("adopted").resolve()
        target_dir = self.game_dir.joinpath("GameData", "XyphosAerospace")
        rm_rf(target_dir)
        shutil.copytree(adopted_path.joinpath(
            "GameData", "XyphosAerospace"), target_dir)
        target_dir = self.game_dir.joinpath("GameData", "IndicatorLightsCommunityExtensions")
        rm_rf(target_dir)
        shutil.copytree(adopted_path.joinpath(
            "GameData", "IndicatorLightsCommunityExtensions"), target_dir)
        target_dir = self.game_dir.joinpath("GameData", "NFEOutdated")
        rm_rf(target_dir)
        shutil.copytree(adopted_path.joinpath(
            "GameData", "NFEOutdated"), target_dir)

    def check_installed(self):
        target_dir = self.game_dir.joinpath("GameData", "XyphosAerospace")
        return target_dir.exists()
