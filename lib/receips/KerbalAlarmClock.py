import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf

def build(game_dir, project_dir):
    src_dir = SourceDir(game_dir, project_dir.joinpath("KerbalAlarmClock"))
    src_dir.output = project_dir.joinpath("PlugInFiles", "GameData", "TriggerTech", "KerbalAlarmClock", "KerbalAlarmClock.dll")
 
    logging.info("  Build Release")
    src_dir.std_compile(
        references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])


def install(game_dir, project_dir):
    target_dir = game_dir.joinpath("GameData", "TriggerTech")
    rm_rf(target_dir)
    shutil.copytree(project_dir.joinpath("PlugInFiles", "GameData", "TriggerTech"), target_dir)


def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "TriggerTech")
    return target_dir.exists()
    