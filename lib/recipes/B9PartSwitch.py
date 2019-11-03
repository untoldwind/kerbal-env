import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt

class B9PartSwitch(Receipt):
    depends = ["ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("B9PartSwitch" ))
        self.source_dir.output = project_dir.joinpath("GameData", "B9PartSwitch", "B9PartSwitch.dll")
        self.target_dir = game_dir.joinpath("GameData", "B9PartSwitch")

    def build(self):
        logging.info("  Build Release")
        rm(self.project_dir.joinpath("GameData", "B9PartSwitch"), "*.ddl")
        self.source_dir.std_compile(
            exclude="**/SubtypePartFields.cs",
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "B9PartSwitch"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
