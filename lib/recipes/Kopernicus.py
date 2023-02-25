import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt

class Kopernicus(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.target_dir = game_dir.joinpath("GameData", "Kopernicus")
        self.target_dir1 = game_dir.joinpath("GameData", "ModularFlightIntegrator")
        self.target_dir2 = game_dir.joinpath("GameData", "000_Harmony")

    def build(self):
        pass
    
    def can_install(self):
        return True

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("GameData", "Kopernicus"), self.target_dir)
        shutil.copytree(self.project_dir.joinpath("GameData", "ModularFlightIntegrator"), self.target_dir1)
        shutil.copytree(self.project_dir.joinpath("GameData", "000_Harmony"), self.target_dir2)

    def check_installed(self):
        return self.target_dir.exists()
