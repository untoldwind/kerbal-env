import logging
from lib.exec import run_command
from lib.utils import rm_rf
from os import path

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
    rm_rf(path.join(game_dir, "GameData", "Kopernicus"))
    rm_rf(path.join(game_dir, "GameData", "ModularFlightIntegrator"))
    run_command(cwd=project_dir, command=["cp", "-r", "./build/GameData/Kopernicus", "%s/GameData" % game_dir])
    run_command(cwd=project_dir, command=["cp", "-r", "./build/GameData/ModularFlightIntegrator", "%s/GameData" % game_dir])

def check_installed(game_dir):
    return False
