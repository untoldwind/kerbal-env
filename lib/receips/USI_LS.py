import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf, rm
from lib.receips import Receipt


class USI_LS(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source", "USILifeSupport"))
        self.for_release_dir = project_dir.joinpath("FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "LifeSupport")
        self.source_dir.output = self.for_release_dir.joinpath("USILifeSupport.dll")
        self.target_dir = game_dir.joinpath("GameData", "UmbraSpaceIndustries", "LifeSupport")
        self.usitools_lib = project_dir.parent.joinpath("USITools", "FOR_RELEASE", "GameData", "000_USITools", "USITools.dll")

    def build(self):
        logging.info("  Build Release")
        rm(self.for_release_dir, "*.dll")
        rm(self.for_release_dir, "*.mdb")
        rm(self.for_release_dir, "*.pdb")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.usitools_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.for_release_dir, self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
