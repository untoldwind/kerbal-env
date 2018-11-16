import logging
import shutil
from lib.utils import mkdir_p, rm_rf

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.for_release_dir = project_dir.joinpath("FOR_RELEASE", "GameData", "UmbraSpaceIndustries")
        self.target_dir = game_dir.joinpath("GameData", "UmbraSpaceIndustries")
        self.subdirs = ["FX", "Kontainers", "ReactorPack"]

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        for subdir in self.subdirs:
            rm_rf(self.target_dir.joinpath(subdir))
            shutil.copytree(self.for_release_dir.joinpath(subdir), self.target_dir.joinpath(subdir))


    def check_installed(self):
        return all(self.target_dir.joinpath(subdir).exists() for subdir in self.subdirs)
