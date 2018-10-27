import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm


def build(game_dir, project_dir):
    src_dir = SourceDir(game_dir, project_dir)
    src_dir.nuget_restore()

    main_src_dir = src_dir.sub_dir("ModuleManager")
    target_dir = main_src_dir.ensure_dir("bin")
    main_src_dir.output = target_dir.joinpath("ModuleManager.dll")
    logging.info("  Build Release")
    main_src_dir.std_compile(
        references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])


def install(game_dir, project_dir):
    gamedata_dir = game_dir.joinpath("GameData")
    rm(gamedata_dir, "ModuleManager*.dll")
    shutil.copy(project_dir.joinpath("ModuleManager",
                                     "bin", "ModuleManager.dll"), gamedata_dir)


def check_installed(game_dir):
    game_dir.joinpath("GameData", "ModuleManager.dll").exists()
