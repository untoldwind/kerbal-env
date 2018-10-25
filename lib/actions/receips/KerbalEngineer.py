import logging
import shutil
from lib.exec import run_command
from lib.utils import rm_rf, rm

def build(game_dir, project_dir):
    src1_dir = project_dir.joinpath("KerbalEngineer")
    src2_dir = project_dir.joinpath("KerbalEngineer.Unity")
    logging.info("  Build Release")
    run_command(cwd=src1_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:PostBuildEvent=",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])
    run_command(cwd=src2_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:PostBuildEvent=",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])


def install(game_dir, project_dir):
    target_dir = game_dir.joinpath("GameData", "KerbalEngineer")
    rm_rf(target_dir)
    shutil.copytree(project_dir.joinpath("Output", "KerbalEngineer"), target_dir)
    rm(target_dir, "MiniAVC.dll")
    rm(target_dir, "Mono.Security.dll")
    rm(target_dir, "System.Core.dll")

def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "KerbalEngineer")
    return target_dir.exists()
    