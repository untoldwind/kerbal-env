from os import path, curdir
from lib.exec import run_command


def build(game_dir, project_dir):
    pass


def install(game_dir, project_dir):
    adopted_path = path.join(curdir, "adopted")
    run_command(cwd=adopted_path, command=[
                "cp", "-r", "GameData/XyphosAerospace", "%s/GameData" % game_dir])
