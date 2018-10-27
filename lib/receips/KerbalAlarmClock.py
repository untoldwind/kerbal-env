import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir

    def build(self):
        src_dir = SourceDir(
            self.game_dir, self.project_dir.joinpath("KerbalAlarmClock"))
        src_dir.output = self.project_dir.joinpath(
            "PlugInFiles", "GameData", "TriggerTech", "KerbalAlarmClock", "KerbalAlarmClock.dll")

        logging.info("  Build Release")
        src_dir.std_compile(
            references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def install(self):
        target_dir = self.game_dir.joinpath("GameData", "TriggerTech")
        rm_rf(target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "PlugInFiles", "GameData", "TriggerTech"), target_dir)

    def check_installed(self):
        target_dir = self.game_dir.joinpath("GameData", "TriggerTech")
        return target_dir.exists()
