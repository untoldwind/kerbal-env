import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source" ))
        self.source_dir.output = project_dir.joinpath("Binaries", "KIS.dll")
        self.target_dir = game_dir.joinpath("GameData", "EnvironmentalVisualEnhancements")

    def build(self):
        pass

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("GameData", "EnvironmentalVisualEnhancements"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
