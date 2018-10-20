import logging
from lib.exec import run_command
from os import path
from lib.utils import ln_s, exists, rm_rf


def build(game_dir, project_dir):
    src_dir = path.join(project_dir, "src")
    logging.info("  nuget restore")
    run_command(cwd=src_dir,  command=["nuget", "restore"])
    run_command(cwd=src_dir,  command=[
                "nuget", "install", "NUnit.Runners", "-Version", "2.6.4"])
    logging.info("  Build tests")
    run_command(cwd=src_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Debug",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])
    logging.info("  Run tests")
    run_command(cwd=src_dir, command=[
                "mono", "./NUnit.Runners.2.6.4/tools/nunit-console.exe", "kOS.Safe.Test/bin/Debug/kOS.Safe.Test.dll"])
    logging.info("  Build Release")
    run_command(cwd=src_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])

def install(game_dir, project_dir):
    rm_rf(path.join(game_dir, "GameData", "kOS"))
    run_command(cwd=project_dir, command=["cp", "-r", "./Resources/GameData/kOS", "%s/GameData" % game_dir])

def check_installed(game_dir):
    return False
