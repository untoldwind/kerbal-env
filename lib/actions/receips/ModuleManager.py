from lib.exec import run_command

def build(game_dir, project_dir):
    run_command(cwd=project_dir,  command=["nuget", "restore"])
    run_command(cwd=project_dir,  command=[
                "msbuild", "/target:Build", "/property:Configuration=Release",
                "/property:ReferencePath=%s/KSP_Data/Managed" % game_dir])
