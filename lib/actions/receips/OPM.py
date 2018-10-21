from lib.exec import run_command
from lib.utils import rm_rf
from os import path

def build(game_dir, project_dir):
    pass


def install(game_dir, project_dir):
    rm_rf(path.join(game_dir, "GameData", "OPM"))
    rm_rf(path.join(game_dir, "GameData", "CTTP"))
    run_command(cwd=project_dir, command=["cp", "-r", "./GameData/OPM", "%s/GameData" % game_dir])
    run_command(cwd=project_dir, command=["cp", "-r", "./GameData/CTTP", "%s/GameData" % game_dir])

def check_installed(game_dir):
    return False
    