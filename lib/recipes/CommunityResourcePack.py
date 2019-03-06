import shutil
from lib.utils import rm_rf
from lib.recipes import Receipt

class CommunityResourcePack(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.target_dir = game_dir.joinpath("GameData", "CommunityResourcePack")

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("FOR_RELEASE", "GameData", "CommunityResourcePack"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
