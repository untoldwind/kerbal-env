import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt

class AVP(Receipt):
    depends = ["ModuleManager", "EnvironmentalVisualEnhancements", "scatterer", "TextureReplacer"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.target_dir = game_dir.joinpath("GameData", "AstronomersVisualPack")

    def build(self):
        pass
    
    def can_install(self):
        return True

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("GameData", "AstronomersVisualPack"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
