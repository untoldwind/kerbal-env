import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.receips import Receipt


class MKS(Receipt):
    depends = ["ModuleManager", "GroundConstruction",
               "USITools", "USI_Core", "FireSpitterCore"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath(
            "Source", "KolonyTools", "KolonyTools"))
        self.for_release_dir = project_dir.joinpath(
            "FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "MKS")
        self.source_dir.output = self.for_release_dir.joinpath(
            "KolonyTools.dll")
        self.target_dir1 = game_dir.joinpath(
            "GameData", "UmbraSpaceIndustries", "MKS")
        self.target_dir2 = game_dir.joinpath(
            "GameData", "UmbraSpaceIndustries", "Karibou")
        self.usitool_lib = project_dir.parent.joinpath(
            "USITools", "FOR_RELEASE", "GameData", "000_USITools", "USITools.dll")

    def build(self):
        logging.info("  Build Release")
        rm(self.for_release_dir, "*.dll")
        rm(self.for_release_dir, "*.mdb")
        rm(self.for_release_dir, "*.pdb")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.usitool_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir1)
        rm_rf(self.target_dir2)
        shutil.copytree(self.project_dir.joinpath(
            "FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "MKS"), self.target_dir1)
        shutil.copytree(self.project_dir.joinpath(
            "FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "Karibou"), self.target_dir2)

    def check_installed(self):
        return self.target_dir1.exists() and self.target_dir2.exists()
