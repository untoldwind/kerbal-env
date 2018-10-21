import logging
from lib.exec import run_command
from lib.utils import mkdir_p, exists
from os import path
from .receips import find_receipt



def install_mod(name, config):
    build_dir = path.join(path.curdir, "build")
    project_dir = path.join(build_dir, name)
    receipt = find_receipt(name)
    logging.info("Running install receipt: %s" % name)
    receipt.install(config.game_dir, project_dir)
