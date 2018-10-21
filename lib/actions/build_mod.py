import logging
from lib.exec import run_command
from lib.utils import mkdir_p, exists
from os import path
from .receips import find_receipt


def build_mod(name, config):
    build_dir = path.join(path.curdir, "build")
    project_dir = path.join(build_dir, name)
    if not exists(project_dir):
        mkdir_p(project_dir)
        if config.source_type == "git":
            logging.info("Checking out %s to: %s" % (config.source, build_dir))
            run_command(cwd=build_dir, command=[
                        "git", "clone", config.source])
            run_command(cwd=project_dir, command=[
                        "git", "checkout", config.checkout])
    else:
        if config.source_type == "git":
            logging.info("Updating %s" % config.source)
            run_command(cwd = project_dir, command = ["git", "checkout", config.checkout])
            run_command(cwd = project_dir, command = ["git", "pull"])
    receipt = find_receipt(name)
    logging.info("Running build receipt: %s" % name)
    receipt.build(config.game_dir, project_dir)
