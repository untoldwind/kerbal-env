from lib.exec import run_command
from lib.utils import rm
from os import path


def build(game_dir, project_dir):
    run_command(cwd=project_dir,  command=["nuget", "restore"])
    run_command(cwd=project_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])


def install(game_dir, project_dir):
    rm(path.join(game_dir, "GameData"), "ModuleManager*.dll")
    run_command(cwd=project_dir, command=[
                "cp", "./ModuleManager/bin/Release/ModuleManager.dll", "%s/GameData" % game_dir])

def check_installed(game_dir):
    return False
