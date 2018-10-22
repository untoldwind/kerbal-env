import logging
import shutil
from lib.exec import run_command
from lib.utils import mkdir_p, rm_rf

def build(game_dir, project_dir):
    logging.info("  Build Release")
    run_command(cwd=project_dir,  command=[
        "mcs", "-unsafe", "-t:library", "-lib:%s/KSP_Data/Managed" % game_dir, "-r:Assembly-CSharp,Assembly-CSharp-firstpass,UnityEngine", 
        "CustomBarnKit.cs", "CustomGameVariables.cs", "Detourer.cs", "Properties/AssemblyInfo.cs"])

def install(game_dir, project_dir):
    target_dir = game_dir.joinpath("GameData", "CustomBarnKit")
    rm_rf(target_dir)
    mkdir_p(target_dir)
    shutil.copy(project_dir.joinpath("CustomBarnKit.dll"), target_dir)
    shutil.copy(project_dir.joinpath("CustomBarnKit", "default.cfg"), target_dir)

def check_installed(game_dir):
    target_dir = game_dir.joinpath("GameData", "CustomBarnKit")
    return target_dir.exists()

    