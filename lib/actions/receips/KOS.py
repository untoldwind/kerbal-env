from lib.exec import run_command
from os import path
from lib.utils import ln_s, exists

def build(game_dir, project_dir, debug):
    src_dir = path.join(project_dir, "src")
    run_command(cwd = src_dir,  command = ["nuget", "restore"], debug = debug)
    for lib_name in ["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"]:
        source = path.join(game_dir, "KSP_Data", "Managed", lib_name)
        target = path.join(project_dir, "Resources", lib_name)
        if not exists(target):
            ln_s(source, target)
    run_command(cwd = src_dir,  command = ["msbuild", "/target:Build", "/property:Configuration=Release"], debug = debug)
