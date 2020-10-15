import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt

class AVP_Textures(Receipt):
    depends = ["AVP"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.target_dir1 = game_dir.joinpath("GameData", "AstronomersVisualPack", "AVP_Configs", "Textures")
        self.target_dir2 = game_dir.joinpath("GameData", "AstronomersVisualPack", "AVP_Skybox", "Skybox")

    def build(self):
        pass
    
    def can_install(self):
        return True

    def install(self):
        rm_rf(self.target_dir1)
        rm_rf(self.target_dir2)
        shutil.copytree(self.project_dir.joinpath("GameData", "AstronomersVisualPack", "AVP_Configs", "Textures"), self.target_dir1)
        shutil.copytree(self.project_dir.joinpath("GameData", "AstronomersVisualPack", "AVP_Skybox", "Skybox"), self.target_dir2)

    def check_installed(self):
        return self.target_dir1.exists() and self.target_dir2.exists()
