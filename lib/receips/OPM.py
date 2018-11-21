import shutil
from lib.exec import run_command
from lib.utils import rm_rf
from lib.receips import Receipt


class OPM(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        target_dir1 = self.game_dir.joinpath("GameData", "OPM")
        target_dir2 = self.game_dir.joinpath("GameData", "CTTP")
        rm_rf(target_dir1)
        rm_rf(target_dir2)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "OPM"), target_dir1)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "CTTP"), target_dir2)

    def check_installed(self):
        target_dir1 = self.game_dir.joinpath("GameData", "OPM")
        return target_dir1.exists()
