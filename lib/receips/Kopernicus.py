import logging
import shutil
from lib.exec import run_command
from lib.utils import rm_rf


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir

    def build(self):
        logging.info("  git submodules")
        run_command(cwd=self.project_dir, command=["git", "submodule", "init"])
        run_command(cwd=self.project_dir, command=[
                    "git", "submodule", "update"])
        logging.info("  nuget restore")
        run_command(cwd=self.project_dir,  command=["nuget", "restore"])
        logging.info("  Build Release")
        run_command(cwd=self.project_dir,  command=[
                    "msbuild", "/target:Build", "/property:Configuration=Release"])

    def can_install(self):
        self.project_dir.joinpath(
                    "build", "GameData", "ModularFlightIntegrator", "ModularFlightIntegrator.dll").exists()

    def install(self):
        target_dir1 = self.game_dir.joinpath("GameData", "Kopernicus")
        target_dir2 = self.game_dir.joinpath(
            "GameData", "ModularFlightIntegrator")
        rm_rf(target_dir1)
        rm_rf(target_dir2)
        shutil.copytree(self.project_dir.joinpath(
            "build", "GameData", "Kopernicus"), target_dir1)
        shutil.copytree(self.project_dir.joinpath(
            "build", "GameData", "ModularFlightIntegrator"), target_dir2)

    def check_installed(self):
        target_dir1 = self.game_dir.joinpath("GameData", "Kopernicus")
        return target_dir1.exists()
