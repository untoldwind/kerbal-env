import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf, rm


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("USITools", "USITools"))
        self.for_release_dir = project_dir.joinpath("FOR_RELEASE", "GameData", "000_USITools")
        self.source_dir.output = self.for_release_dir.joinpath("USITools.dll")
        self.target_dir = game_dir.joinpath("GameData", "000_USITools")

    def build(self):
        logging.info("  Build Release")
        rm(self.for_release_dir, "*.dll")
        rm(self.for_release_dir, "*.mdb")
        rm(self.for_release_dir, "*.pdb")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.for_release_dir, self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
