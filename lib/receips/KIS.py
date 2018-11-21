import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.receips import Receipt

class KIS(Receipt):
    depends = ["CommunityCategoryKit", "KSPDev"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source" ))
        self.source_dir.output = project_dir.joinpath("Binaries", "KIS.dll")
        self.ksp_dev_lib = project_dir.parent.joinpath("KSPDev", "Binaries", "KSPDev_Utils.0.37.dll")
        self.target_dir = game_dir.joinpath("GameData", "KIS")

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.ksp_dev_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        mkdir_p(self.target_dir)
        for sub_dir in ["Lang", "Parts", "Patches", "Sounds", "Textures"]:
            shutil.copytree(self.project_dir.joinpath(sub_dir), self.target_dir.joinpath(sub_dir))
        shutil.copy(self.project_dir.joinpath("User Guide.pdf"), self.target_dir)
        shutil.copy(self.project_dir.joinpath("settings.cfg"), self.target_dir)
        mkdir_p(self.target_dir.joinpath("Plugins"))
        shutil.copy(self.source_dir.output, self.target_dir.joinpath("Plugins"))
        shutil.copy(self.ksp_dev_lib, self.target_dir.joinpath("Plugins"))


    def check_installed(self):
        return self.target_dir.exists()
