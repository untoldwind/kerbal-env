import shutil
from lib.recipes import Receipt
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm

class ModularFlightIntegrator(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir)
        self.target_dir = game_dir.joinpath("GameData", "ModularFlightIntegrator")
        self.output_dir = self.project_dir.joinpath("obj")
        self.source_dir.output = self.output_dir.joinpath("ModularFlightIntegrator.dll")

    def build(self):
        rm_rf(self.output_dir)
        mkdir_p(self.output_dir)
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.CoreModule.dll", "UnityEngine.AnimationModule.dll", "UnityEngine.InputLegacyModule.dll", "UnityEngine.IMGUIModule.dll", "UnityEngine.PhysicsModule.dll", "UnityEngine.UI.dll", "UnityEngine.JSONSerializeModule.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        mkdir_p(self.target_dir)
        rm(self.target_dir, "*.dll")
        shutil.copy(self.source_dir.output, self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
