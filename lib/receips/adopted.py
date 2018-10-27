import shutil
import pathlib
from lib.utils import rm_rf

def build(game_dir, project_dir):
    pass


def install(game_dir, project_dir):
    adopted_path = pathlib.Path().joinpath("adopted").resolve()
    target_dir = game_dir.joinpath("GameData", "XyphosAerospace")
    rm_rf(target_dir)
    shutil.copytree(adopted_path.joinpath("GameData", "XyphosAerospace"), target_dir)

def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "XyphosAerospace")
    return target_dir.exists()

