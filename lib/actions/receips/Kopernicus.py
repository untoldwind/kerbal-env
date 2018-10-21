import logging
from lib.exec import run_command

def build(game_dir, project_dir):
    logging.info("  git submodules")
    run_command(cwd=project_dir, command=["git", "submodule", "init"])
    run_command(cwd=project_dir, command=["git", "submodule", "update"])
    logging.info("  nuget restore")
    run_command(cwd=project_dir,  command=["nuget", "restore"])
    logging.info("  Build Release")
    run_command(cwd=project_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release"])

def check_installed(game_dir):
    return False
