import logging
import shutil
from lib.exec import SourceDir
from lib.utils import ln_s, rm_rf, rm, mkdir_p
from lib.recipes import Receipt

class CustomAsteroids(Receipt):
    depends = ["ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("src" ))
        self.source_dir.output = project_dir.joinpath("build", "CustomAsteroids.dll")
        self.target_dir = game_dir.joinpath("GameData", "CustomAsteroids")

    def build(self):
        logging.info("  Build Release")
        mkdir_p(self.project_dir.joinpath("build"))
        self.source_dir.std_compile(
            exclude="tests/**/*",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        mkdir_p(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("Parts"), self.target_dir.joinpath("Parts"))
        shutil.copytree(self.project_dir.joinpath("Resources"), self.target_dir.joinpath("Resources"))
        shutil.copytree(self.project_dir.joinpath("config"), self.target_dir.joinpath("config"))
        shutil.copytree(self.project_dir.joinpath("Localization"), self.target_dir.joinpath("Localization"))
        shutil.copy(self.source_dir.output, self.target_dir)
        shutil.copy(self.project_dir.joinpath("CustomAsteroids.version"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
