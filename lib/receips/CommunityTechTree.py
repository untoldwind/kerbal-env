import shutil
from lib.utils import rm_rf

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.target_dir = game_dir.joinpath("GameData", "CommunityTechTree")

    def build(self):
        pass

    def can_install(self):
        return True

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("GameData", "CommunityTechTree"), self.target_dir)
        rm_rf(self.target_dir.joinpath("Versioning"))


    def check_installed(self):
        return self.target_dir.exists()
