import logging
from lib.exec import run_command
from lib.utils import mkdir_p, rm


def run(config):
    logging.info("Installing base game to: %s" % config.target_dir)

    mkdir_p(config.target_dir)
    run_command(cwd=config.target_dir, command=[
                "unzip", config.install_base])

    logging.info("Adding DLC1 (Making history)")
    run_command(cwd=config.game_dir, command=[
                "unzip", config.install_dlc1])
    run_command(cwd=config.game_dir, command=[
                "./dlc-mhe-en-us.sh"])
    rm(config.game_dir, "*.sh")
    rm(config.game_dir, "*.zip")
