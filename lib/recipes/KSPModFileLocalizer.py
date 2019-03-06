import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf, rm
from lib.recipes import Receipt


class KSPModFileLocalizer(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Sources", "KSPModFileLocalizer"))
        self.for_release_dir = self.project_dir.joinpath("FOR_RELEASE")
        self.source_dir.output = self.for_release_dir.joinpath("KSPModFileLocalizer.dll")
        self.target_file = game_dir.joinpath("GameData", "KSPModFileLocalizer.dll")

    def build(self):
        logging.info("  Build Release")
        rm(self.for_release_dir, "*.dll")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_file)
        shutil.copy(self.source_dir.output, self.target_file)

    def check_installed(self):
        return self.target_file.exists()
