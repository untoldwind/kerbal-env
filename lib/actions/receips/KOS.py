import logging
import shutil
from lib.exec import run_command
from lib.utils import ln_s, rm_rf


def build(game_dir, project_dir):
    src_dir = project_dir.joinpath("src")
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
    target_dir = game_dir.joinpath("GameData", "kOS")
    rm_rf(target_dir)
    shutil.copytree(project_dir.joinpath("Resources", "GameData", "kOS"), target_dir)

def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "kOS")
    return target_dir.exists()
