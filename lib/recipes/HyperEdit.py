import shutil
from lib.recipes import Receipt
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm

class HyperEdit(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source"))
        self.target_dir = game_dir.joinpath("GameData", "Kerbaltek")

    def build(self):
        output_dir = self.project_dir.joinpath("obj")
        rm_rf(output_dir)
        mkdir_p(output_dir)
        self.source_dir.output = output_dir.joinpath("HyperEdit.dll")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.CoreModule.dll", "UnityEngine.AnimationModule.dll", "UnityEngine.InputLegacyModule.dll", "UnityEngine.IMGUIModule.dll", "UnityEngine.PhysicsModule.dll", "UnityEngine.UI.dll", "UnityEngine.JSONSerializeModule.dll"])

    def can_install(self):
        return self.project_dir.joinpath("obj", "HyperEdit.dll").exists()

    def install(self):
        mkdir_p(self.target_dir)
        mkdir_p(self.target_dir.joinpath("HyperEdit"))
        rm(self.target_dir, "*.dll")
        shutil.copy(self.project_dir.joinpath("obj", "HyperEdit.dll"), self.target_dir)
        shutil.copy(self.project_dir.joinpath("HyperEdit.version"), self.target_dir.joinpath("HyperEdit"))

    def check_installed(self):
        return self.target_dir.exists()
