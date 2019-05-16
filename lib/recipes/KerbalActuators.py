import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt


class KerbalActuators(Receipt):
    depends = ["ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(
            game_dir, project_dir.joinpath("KerbalActuators"))
        self.plugins_dir = project_dir.joinpath(
            "GameData", "WildBlueIndustries", "001KerbalActuators", "Plugins")
        self.source_dir.output = self.plugins_dir.joinpath(
            "KerbalActuators.dll")
        self.target_dir = game_dir.joinpath("GameData", "WildBlueIndustries", "001KerbalActuators")

    def build(self):
        rm(self.plugins_dir, "*.dll")
        self.source_dir.std_compile(
            exclude=[
                "WBIAirParkPartModule.cs",
                "Controllers/WBIRCSPropSpinner.cs",
            ],
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "WildBlueIndustries", "001KerbalActuators"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
