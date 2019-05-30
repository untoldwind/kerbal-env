import logging
from lib.exec import run_command
from lib.utils import mkdir_p, rm


def install_game(config):
    logging.info("Installing base game to: %s" % config.target_dir)

    mkdir_p(config.target_dir)
    run_command(cwd=config.target_dir, command=[
                "unzip", "-qo", config.install_base])

    if config.has_dlc1:
        logging.info("Adding DLC1 (Making history)")
        run_command(cwd=config.game_dir, command=[
                    "unzip", "-qo", config.install_dlc1])
        run_command(cwd=config.game_dir, command=[
                    "./dlc-mhe-en-us.sh"])
        rm(config.game_dir, "*.sh")
        rm(config.game_dir, "*.zip")

    if config.has_dlc2:
        logging.info("Adding DLC2 (Breaking Grounds)")
        run_command(cwd=config.game_dir, command=[
                    "unzip", "-qo", config.install_dlc2])
        run_command(cwd=config.game_dir, command=[
                    "./dlc-bge-en-us.sh"])
        rm(config.game_dir, "*.sh")
        rm(config.game_dir, "*.zip")

def check_game_installed(config):
    return config.game_dir.exists() and (not config.has_dlc1 or config.game_dir.joinpath("GameData", "SquadExpansion").exists())

