from termcolor import colored
from .install_game import check_game_installed
from lib.recipes import find_receipt
import pathlib

def status(config):
    installed_or_not("Game", check_game_installed(config))
    sorted_names = sorted(config.mods.keys())
    build_dir = pathlib.Path().joinpath("build").resolve()

    print()
    for name in sorted_names:
        receipt = find_receipt(name, config.game_dir, build_dir)
        installed_or_not(name, receipt.check_installed(), enabled = config.mods[name].enabled)

def installed_or_not(name, installed, enabled = True):
    if installed:
        print("%-40s: %s" % (name, colored("INSTALLED", "green")))
    elif not enabled:
        print("%-40s: %s" % (name, colored("DISABLED", "yellow")))
    else:
        print("%-40s: %s" % (name, colored("NOT INSTALLED", "red")))