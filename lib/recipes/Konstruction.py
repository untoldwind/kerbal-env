import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf, rm
from lib.recipes import Receipt

class Konstruction(Receipt):
    depends = ["CommunityResourcePack", "USITools"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source", "Konstruction"))
        self.for_release_dir1 = project_dir.joinpath("FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "Konstruction")
        self.for_release_dir2 = project_dir.joinpath("FOR_RELEASE", "GameData", "UmbraSpaceIndustries", "Akita")
        self.source_dir.output = self.for_release_dir1.joinpath("Konstruction.dll")
        self.target_dir1 = game_dir.joinpath("GameData", "UmbraSpaceIndustries", "Konstruction")
        self.target_dir2 = game_dir.joinpath("GameData", "UmbraSpaceIndustries", "Akita")
        self.usitools_lib = project_dir.parent.joinpath("USITools", "FOR_RELEASE", "GameData", "000_USITools", "USITools.dll")

    def build(self):
        logging.info("  Build Release")
        rm(self.for_release_dir1, "*.dll")
        rm(self.for_release_dir1, "*.mdb")
        rm(self.for_release_dir1, "*.pdb")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.AnimationModule.dll", 
                        "UnityEngine.ImageConversionModule.dll",
                        "UnityEngine.IMGUIModule.dll", 
                        "UnityEngine.PhysicsModule.dll",
                        "UnityEngine.UI.dll", self.usitools_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir1)
        rm_rf(self.target_dir2)
        shutil.copytree(self.for_release_dir1, self.target_dir1)
        shutil.copytree(self.for_release_dir2, self.target_dir2)

    def check_installed(self):
        return self.target_dir1.exists() and self.target_dir2.exists()
