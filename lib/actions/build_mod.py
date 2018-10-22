import logging
import patch
import pathlib
import wget
from lib.exec import run_command
from lib.utils import mkdir_p, rm_rf
from .receips import find_receipt


def build_mod(name, config, update):
    build_dir = pathlib.Path().joinpath("build").resolve()
    project_dir = build_dir.joinpath(name)
    if not project_dir.exists():
        initialize_project(build_dir, project_dir, name, config)
    elif update:
        update_project(build_dir, project_dir, name, config)
    if config.patch != None:
        pset = patch.fromstring(config.patch.encode('utf-8'))
        logging.info("Applying patch")
        pset.apply(strip=1, root=project_dir)
    receipt = find_receipt(name)
    logging.info("Running build receipt: %s" % name)
    receipt.build(config.game_dir, project_dir)


def initialize_project(build_dir, project_dir, name, config):
    if config.source_type == "git":
        logging.info("Checking out %s to: %s" % (config.source, build_dir))
        run_command(cwd=build_dir, command=[
                    "git", "clone", config.source, name])
        run_command(cwd=project_dir, command=[
                    "git", "checkout", config.checkout])
    elif config.source_type == "http":
        mkdir_p(project_dir)
        download_dir = pathlib.Path().joinpath("downloads").resolve()
        mkdir_p(download_dir)
        package_file = download_dir.joinpath("%s-%s.zip" % (name, config.version))
        if not package_file.exists():
            logging.info("Downloading %s to %s" % (config.source, package_file))
            wget.download(config.source, package_file)
        run_command(cwd=project_dir, command = ["unzip", package_file])


def update_project(build_dir, project_dir, name, config):
    if config.source_type == "git":
        logging.info("Updating %s" % config.source)
        run_command(cwd=project_dir, command=["git", "checkout", "master"])
        run_command(cwd=project_dir, command=["git", "pull"])
        run_command(cwd=project_dir, command=[
                    "git", "checkout", config.checkout])
    elif config.source_type == "http":
        rm_rf(project_dir)
        initialize_project(build_dir, project_dir, name, config)
        
