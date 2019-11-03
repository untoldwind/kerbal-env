import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm
from lib.recipes import Receipt


class ModuleManager(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.src_dir = SourceDir(self.game_dir, self.project_dir)

    def build(self):
        self.src_dir.nuget_restore()

        main_src_dir = self.src_dir.sub_dir("ModuleManager")
        target_dir = main_src_dir.ensure_dir("bin")
        main_src_dir.output = target_dir.joinpath("ModuleManager.dll")
        logging.info("  Build Release")
        main_src_dir.std_compile(
            references=["Assembly-CSharp.dll", "UnityEngine.dll", "UnityEngine.CoreModule.dll", "UnityEngine.Physics2DModule.dll", "UnityEngine.UI.dll", "UnityEngine.InputLegacyModule.dll", "UnityEngine.ImageConversionModule.dll", "UnityEngine.UIModule.dll", "UnityEngine.TextRenderingModule.dll"])

    def can_install(self):
        return self.project_dir.joinpath("ModuleManager", "bin", "ModuleManager.dll").exists()
        
    def install(self):
        gamedata_dir = self.game_dir.joinpath("GameData")
        rm(gamedata_dir, "ModuleManager*.dll")
        shutil.copy(self.project_dir.joinpath("ModuleManager",
                                              "bin", "ModuleManager.dll"), gamedata_dir)

    def check_installed(self):
        return self.game_dir.joinpath("GameData", "ModuleManager.dll").exists()
