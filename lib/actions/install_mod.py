import logging
import pathlib
from lib.exec import run_command
from lib.utils import mkdir_p
from lib.receips import find_receipt



def install_mod(name, config):
    build_dir = pathlib.Path().joinpath("build").resolve()
    project_dir = build_dir.joinpath(name)
    receipt = find_receipt(name, config.game_dir, project_dir)
    logging.info("Running install receipt: %s" % name)
    receipt.install()
