import logging
import shutil
from lib.exec import SourceDir
from lib.utils import ln_s, rm_rf, rm, mkdir_p
from lib.recipes import Receipt

class FTT(Receipt):
    depends = ["CommunityCategoryKit", "CommunityResourcePack", "USITools"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.target_dir = game_dir.joinpath("GameData", "UmbraSpaceIndustries", "FTT")

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "FTT"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
