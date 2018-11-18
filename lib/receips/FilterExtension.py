import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("FilterExtension"))
        self.plugins_dir = project_dir.joinpath("GameData", "000_FilterExtensions", "Plugins")
        self.source_dir.output = self.plugins_dir.joinpath("FilterExtension.dll")
        self.target_dir1 = game_dir.joinpath("GameData", "000_FilterExtensions")
        self.target_dir2 = game_dir.joinpath("GameData", "000_FilterExtensions_Configs")
        self.target_dir3 = game_dir.joinpath("GameData", "zFinal_FilterExtensions")

    def build(self):
        rm(self.plugins_dir, "*.dll")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir1)
        shutil.copytree(self.project_dir.joinpath("GameData", "000_FilterExtensions"), self.target_dir1)
        shutil.copytree(self.project_dir.joinpath("GameData", "000_FilterExtensions_Configs"), self.target_dir2)
        shutil.copytree(self.project_dir.joinpath("GameData", "zFinal_FilterExtensions"), self.target_dir3)

    def check_installed(self):
        return self.target_dir1.exists() and self.target_dir2.exists() and self.target_dir3.exists()
