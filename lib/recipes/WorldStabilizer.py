import shutil
from lib.recipes import Receipt
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm

class WorldStabilizer(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.plugin_dir = project_dir.joinpath("GameData", "WorldStabilizer", "Plugins")
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("WorldStabilizer"))
        self.source_dir.output = self.plugin_dir.joinpath("WorldStabilizer.dll")
        self.target_dir = game_dir.joinpath("GameData", "WorldStabilizer")

    def build(self):
        rm(self.plugin_dir, "*.dll")
        rm(self.plugin_dir, "*.pdb")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "WorldStabilizer"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
