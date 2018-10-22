import logging
import shutil
from lib.exec import run_command
from lib.utils import rm


def build(game_dir, project_dir):
    logging.info("  nuget restore")
    run_command(cwd=project_dir,  command=["nuget", "restore"])
    logging.info("  Build Release")
    run_command(cwd=project_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])


def install(game_dir, project_dir):
    gamedata_dir = game_dir.joinpath("GameData")
    rm(gamedata_dir, "ModuleManager*.dll")
    shutil.copy(project_dir.joinpath("ModuleManager", "bin", "Release", "ModuleManager.dll"), gamedata_dir)

def check_installed(game_dir):
    return False
