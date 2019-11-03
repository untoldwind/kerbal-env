
import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt


class ConfigurableContainers(Receipt):
    depends = ["ModuleManager", "AT_Utils", "AnisotropicPartResizer"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir)
        self.source_dir.output = project_dir.joinpath(
            "GameData", "ConfigurableContainers", "ConfigurableContainers.dll")
        self.target_dir = game_dir.joinpath(
            "GameData", "ConfigurableContainers")
        self.at_utils_lib = project_dir.parent.joinpath(
            "AT_Utils", "GameData", "000_AT_Utils", "Plugins", "000_AT_Utils.dll")
        self.aniso_lib = project_dir.parent.joinpath(
            "AnisotropicPartResizer", "obj", "001_AnisotropicPartResizer.dll")

    def build(self):
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.IMGUIModule.dll",
                        "UnityEngine.UI.dll", self.at_utils_lib, self.aniso_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "ConfigurableContainers"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
