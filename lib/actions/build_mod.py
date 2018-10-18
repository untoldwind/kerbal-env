from lib.exec import run_command
from lib.utils import mkdir_p, exists
from os import path
from .receips import find_receipt

def run(name, config, debug):
    build_dir = path.join(path.curdir, "build")
    project_dir = path.join(build_dir, name)
    if not exists(project_dir):
        mkdir_p(project_dir)
        print("Checking out %s to: %s" % (config.source, build_dir))
        run_command(cwd = build_dir, command = ["git", "clone", config.source], debug = debug)
        run_command(cwd = project_dir, command = ["git", "checkout", config.branch], debug = debug)
    else:
        print("Updating %s" % config.source)
#        run_command(cwd = project_dir, command = ["git", "checkout", config.branch], debug = debug)
#        run_command(cwd = project_dir, command = ["git", "pull"], debug = debug)
    receipt = find_receipt(name)
    receipt.build(config.game_dir, project_dir, debug = debug)
