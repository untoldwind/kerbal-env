import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt

class AT_Utils(Receipt):
    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.ui_source_dir = SourceDir(game_dir, project_dir.joinpath("Unity"))
        self.ui_source_dir.output = project_dir.joinpath("GameData", "000_AT_Utils", "Plugins", "0_00_AT_Utils_UI.dll")
        self.source_dir = SourceDir(game_dir, project_dir)
        self.source_dir.output = project_dir.joinpath("GameData", "000_AT_Utils", "Plugins", "000_AT_Utils.dll")
        self.target_dir = game_dir.joinpath("GameData", "000_AT_Utils")

    def build(self):
        logging.info("  Build Release")
        self.ui_source_dir.std_compile(
            exclude="Assets/**/*.cs",
            references=["Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "KSPAssets.dll", 
                        "UnityEngine.dll", 
                        "UnityEngine.AudioModule.dll", 
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.InputLegacyModule.dll",
                        "UnityEngine.UI.dll",
                        "UnityEngine.UIModule.dll"]
        )
        self.source_dir.std_compile(
            exclude=[
                "AnimatedConverters/**/*.cs",
                "SubmodelResizer/**/*.cs",
                "ConfigurableContainers/**/*.cs",
                "AnisotropicPartResizer/**/*.cs",
                "MultiAnimators/**/*.cs",
                "Unity/**/*.cs",
            ],
            references=["Assembly-CSharp.dll",
                        "Assembly-CSharp-firstpass.dll",
                        "KSPAssets.dll", 
                        "UnityEngine.dll",
                        "UnityEngine.CoreModule.dll", 
                        "UnityEngine.AudioModule.dll", 
                        "UnityEngine.AnimationModule.dll", 
                        "UnityEngine.InputLegacyModule.dll",
                        "UnityEngine.ImageConversionModule.dll",
                        "UnityEngine.IMGUIModule.dll", 
                        "UnityEngine.PhysicsModule.dll",
                        "UnityEngine.TextRenderingModule.dll",
                        "UnityEngine.UI.dll", self.ui_source_dir.output]
        )

    def can_install(self):
        return self.source_dir.output.exists() and self.ui_source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        rm(self.project_dir.joinpath("GameData", "000_AT_Utils"), "*.ksp")
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "000_AT_Utils"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
