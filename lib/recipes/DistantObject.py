import logging
import shutil
from lib.exec import SourceDir
from lib.utils import ln_s, rm_rf, rm, mkdir_p
from lib.recipes import Receipt

class DistantObject(Receipt):
    depends = []

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source-Code" ))
        self.source_dir.output = project_dir.joinpath("GameData", "DistantObject", "DistantObject.dll")
        self.target_dir = game_dir.joinpath("GameData", "DistantObject")

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("GameData", "DistantObject"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
