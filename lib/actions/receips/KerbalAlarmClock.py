import logging
import shutil
from lib.exec import run_command
from lib.utils import rm_rf

def build(game_dir, project_dir):
    src_dir = project_dir.joinpath("KerbalAlarmClock")
    logging.info("  Build Release")
    run_command(cwd=src_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:PostBuildEvent=",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])


def install(game_dir, project_dir):
    target_dir = game_dir.joinpath("GameData", "TriggerTech")
    rm_rf(target_dir)
    shutil.copytree(project_dir.joinpath("PlugInFiles", "GameData", "TriggerTech"), target_dir)
    shutil.copy(project_dir.joinpath("KerbalAlarmClock", "bin", "Release", "KerbalAlarmClock.dll"), target_dir.joinpath("KerbalAlarmClock"))
    shutil.copy(project_dir.joinpath("KerbalAlarmClock", "KerbalAlarmClock.version"), target_dir.joinpath("KerbalAlarmClock"))


def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "TriggerTech")
    return target_dir.exists()
    