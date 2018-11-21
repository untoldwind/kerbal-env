import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.receips import Receipt

class DockRotate(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("DockRotate"))
        self.source_dir.output = self.project_dir.joinpath("Resources", "DockRotate.dll")
        self.target_dir = game_dir.joinpath("GameData", "DockRotate")

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("Resources"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
