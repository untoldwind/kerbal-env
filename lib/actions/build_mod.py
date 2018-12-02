import logging
import patch
import pathlib
import wget
from lib.exec import run_command
from lib.utils import mkdir_p, rm_rf
from lib.receips import find_receipt


def build_mod(name, config, update):
    build_dir = pathlib.Path().joinpath("build").resolve()
    mkdir_p(build_dir)
    project_dir = build_dir.joinpath(name)
    apply_patch = False
    if not project_dir.exists():
        initialize_project(build_dir, project_dir, name, config)
        apply_patch = True
    elif update:
        update_project(build_dir, project_dir, name, config)
        apply_patch = True
    if apply_patch and config.patch != None:
        pset = patch.fromstring(config.patch.encode('utf-8'))
        logging.info("Applying patch")
        pset.apply(strip=1, root=project_dir)
    receipt = find_receipt(name, config.game_dir, project_dir)
    logging.info("Running build receipt: %s" % name)
    receipt.build()


def initialize_project(build_dir, project_dir, name, config):
    if config.source_type == "git":
        logging.info("Checking out %s to: %s" % (config.source, build_dir))
        run_command(cwd=build_dir, command=[
                    "git", "clone", "--depth", "1", "-b", config.checkout, config.source, name])
    elif config.source_type == "http":
        mkdir_p(project_dir)
        download_dir = pathlib.Path().joinpath("downloads").resolve()
        mkdir_p(download_dir)
        package_file = download_dir.joinpath("%s-%s.zip" % (name, config.version))
        if not package_file.exists():
            logging.info("Downloading %s to %s" % (config.source, package_file))
            wget.download(config.source, str(package_file))
        run_command(cwd=project_dir, command = ["unzip", package_file])


def update_project(build_dir, project_dir, name, config):
    if config.source_type == "git" and not config.checkout_is_tag:
        logging.info("Updating %s" % config.source)
        run_command(cwd=project_dir, command=["git", "fetch", "--depth", "1", "origin", config.checkout])
        run_command(cwd=project_dir, command=["git", "reset", "--hard", "origin/" + config.checkout])
    elif config.source_type == "http":
        rm_rf(project_dir)
        initialize_project(build_dir, project_dir, name, config)
        
