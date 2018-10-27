import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("SOURCE", "CCK", "CCK"))
        self.source_dir.output = project_dir.joinpath("FOR_RELEASE", "GameData", "CommunityCategoryKit", "CCK.dll")
        self.target_dir = game_dir.joinpath("GameData", "CommunityCategoryKit")

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
           "FOR_RELEASE", "GameData", "CommunityCategoryKit"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()