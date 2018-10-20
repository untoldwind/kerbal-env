from lib.exec import run_command

def build(game_dir, project_dir):
    run_command(cwd=project_dir, command=["git", "submodule", "init"])
    run_command(cwd=project_dir, command=["git", "submodule", "update"])
    run_command(cwd=project_dir,  command=["nuget", "restore"])
    run_command(cwd=project_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release"])

    pass

def check_installed(game_dir):
    return False
