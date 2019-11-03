import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt


class NearFutureProps(Receipt):
    depends=["ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(
            game_dir, project_dir.joinpath("Source", "NFPropUtils"))
        self.plugins_dir = project_dir.joinpath(
            "GameData", "NearFutureProps", "Plugins")
        self.source_dir.output = self.plugins_dir.joinpath("NFPropUtils.dll")
        self.target_dir = game_dir.joinpath("GameData", "NearFutureProps")

    def build(self):
        logging.info("  Build Release")
        rm(self.plugins_dir, "*.dll")
        rm(self.project_dir.joinpath("GameData",
                                     "NearFutureProps", "Versioning"), "*.dll")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.AnimationModule.dll", 
                        "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "NearFutureProps"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
