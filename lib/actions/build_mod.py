import logging
import patch
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
                        "git", "clone", config.source, name])
            run_command(cwd=project_dir, command=[
                        "git", "checkout", config.checkout])
    else:
        if config.source_type == "git":
            logging.info("Updating %s" % config.source)
            run_command(cwd = project_dir, command = ["git", "checkout", "master"])
            run_command(cwd = project_dir, command = ["git", "pull"])            
            run_command(cwd = project_dir, command = ["git", "checkout", config.checkout])
    if config.patch != None:
        pset = patch.fromstring(config.patch.encode('utf-8'))
        logging.info("Applying patch")
        pset.apply(strip=1, root=project_dir)
    receipt = find_receipt(name)
    logging.info("Running build receipt: %s" % name)
    receipt.build(config.game_dir, project_dir)
