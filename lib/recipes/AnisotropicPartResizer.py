import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf
from lib.recipes import Receipt


class AnisotropicPartResizer(Receipt):
    depends=["ModuleManager", "AT_Utils"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir)
        self.source_dir.output = project_dir.joinpath(
            "obj", "001_AnisotropicPartResizer.dll")
        self.target_dir = game_dir.joinpath(
            "GameData", "001_AnisotropicPartResizer")
        self.at_utils_lib = project_dir.parent.joinpath(
            "AT_Utils", "GameData", "000_AT_Utils", "Plugins", "000_AT_Utils.dll")

    def build(self):
        mkdir_p(self.project_dir.joinpath("obj"))
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.UI.dll", self.at_utils_lib])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        mkdir_p(self.target_dir)
        shutil.copy(self.project_dir.joinpath(
            "obj", "001_AnisotropicPartResizer.dll"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
