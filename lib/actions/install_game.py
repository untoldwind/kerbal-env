from lib.exec import run_command
from lib.utils import mkdirp

def run(config, debug):
    print("Installing base game to: %s" % config.target_dir)

#    mkdirp(config.target_dir)
#    run_command(pwd = config.target_dir, command = ["unzip", config.install_base], debug = debug)

    print("Adding DLC1 (Making history)")
#    run_command(pwd = config.game_dir, command = ["unzip", config.install_dlc1], debug = debug)
#    run_command(pwd = config.game_dir, command = ["./dlc-mhe-en-us.sh"], debug = debug)
