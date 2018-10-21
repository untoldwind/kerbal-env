import logging
from lib.exec import run_command
from os import path
from lib.utils import mkdir_p, rm_rf

def build(game_dir, project_dir):
    logging.info("  Build Release")
    run_command(cwd=project_dir,  command=[
        "mcs", "-unsafe", "-t:library", "-lib:%s/KSP_Data/Managed" % game_dir, "-r:Assembly-CSharp,Assembly-CSharp-firstpass,UnityEngine", 
        "CustomBarnKit.cs", "CustomGameVariables.cs", "Detourer.cs", "Properties/AssemblyInfo.cs"])

def install(game_dir, project_dir):
    rm_rf(path.join(game_dir, "GameData", "CustomBarnKit"))
    mkdir_p(path.join(game_dir, "GameData", "CustomBarnKit"))
    run_command(cwd=project_dir, command=["cp", "./CustomBarnKit.dll", "%s/GameData/CustomBarnKit" % game_dir])
    run_command(cwd=project_dir, command=["cp", "./CustomBarnKit/default.cfg", "%s/GameData/CustomBarnKit" % game_dir])

def check_installed(game_dir):
    return False
    