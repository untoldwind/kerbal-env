import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir

    def build(self):
        logging.info("  Build Release")
        src_dir = SourceDir(self.game_dir, self.project_dir)
        target_dir = src_dir.ensure_dir("bin")
        src_dir.output = target_dir.joinpath("CustomBarnKit.dll")
        logging.info("  Build Release")
        src_dir.std_compile(
            references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.UI.dll"], extra_args=["/unsafe"])

    def install(self):
        target_dir = self.game_dir.joinpath("GameData", "CustomBarnKit")
        rm_rf(target_dir)
        mkdir_p(target_dir)
        shutil.copy(self.project_dir.joinpath(
            "bin", "CustomBarnKit.dll"), target_dir)
        shutil.copy(self.project_dir.joinpath(
            "CustomBarnKit", "default.cfg"), target_dir)

    def check_installed(self):
        target_dir = self.game_dir.joinpath("GameData", "CustomBarnKit")
        return target_dir.exists()