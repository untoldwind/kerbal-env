import logging
import shutil
from lib.exec import run_command
from lib.utils import rm_rf


def build(game_dir, project_dir):
    logging.info("  git submodules")
    run_command(cwd=project_dir, command=["git", "submodule", "init"])
    run_command(cwd=project_dir, command=["git", "submodule", "update"])
    logging.info("  nuget restore")
    run_command(cwd=project_dir,  command=["nuget", "restore"])
    logging.info("  Build Release")
    run_command(cwd=project_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release"])

def install(game_dir, project_dir):
    target_dir1 = game_dir.joinpath("GameData", "Kopernicus")
    target_dir2 = game_dir.joinpath("GameData", "ModularFlightIntegrator")
    rm_rf(target_dir1)
    rm_rf(target_dir2)
    shutil.copytree(project_dir.joinpath("build", "GameData", "Kopernicus"), target_dir1)
    shutil.copytree(project_dir.joinpath("build", "GameData", "ModularFlightIntegrator"), target_dir2)

def check_installed(game_dir):
    target_dir1 = game_dir.joinpath("GameData", "Kopernicus")
    return target_dir1.exists()
