import shutil
from lib.exec import run_command
from lib.utils import rm_rf

def build(game_dir, project_dir):
    pass


def install(game_dir, project_dir):
    target_dir1 = game_dir.joinpath("GameData", "OPM")
    target_dir2 = game_dir.joinpath("GameData", "CTTP")
    rm_rf(target_dir1)
    rm_rf(target_dir2)
    shutil.copytree(project_dir.joinpath("GameData", "OPM"), target_dir1)
    shutil.copytree(project_dir.joinpath("GameData", "CTTP"), target_dir2)

def check_installed(game_dir):
    target_dir1 = game_dir.joinpath("GameData", "OPM")
    return target_dir1.exists()
    