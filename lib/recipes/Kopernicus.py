import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import rm_rf
from lib.recipes import Receipt


class Kopernicus(Receipt):
    depends = ["ModuleManager", "ModularFlightIntegrator"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.parser_src = SourceDir(game_dir, project_dir.joinpath("src", "external", "config-parser", "src"))
        self.parser_src.output = project_dir.joinpath("build", "GameData", "Kopernicus", "Plugins", "Kopernicus.Parser.dll")
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("src", "Kopernicus"))
        self.source_dir.output = project_dir.joinpath("build", "GameData", "Kopernicus", "Plugins", "Kopernicus.dll")
        self.mfi_lib = project_dir.parent.joinpath("ModularFlightIntegrator", "obj", "ModularFlightIntegrator.dll")

    def build(self):
        logging.info("  git submodules")
        run_command(cwd=self.project_dir, command=["git", "submodule", "init"])
        run_command(cwd=self.project_dir, command=[
                    "git", "submodule", "update"])
        self.parser_src.std_compile(references=[
            "Assembly-CSharp.dll", 
            "UnityEngine.dll",
            "UnityEngine.CoreModule.dll", 
        ])
        self.source_dir.std_compile(extra_args=["/unsafe"], references=[
            "Assembly-CSharp.dll", 
            "UnityEngine.dll",
            "UnityEngine.AssetBundleModule.dll",
            "UnityEngine.CoreModule.dll",
            "UnityEngine.ImageConversionModule.dll",
            "UnityEngine.ParticleSystemModule.dll",
            "UnityEngine.PhysicsModule.dll",
            "UnityEngine.UI.dll",
            self.mfi_lib,
            self.parser_src.output
        ], exclude=[
            "Components/MaterialWrapper/TerrainGasGiant.cs",
            "Configuration/MaterialLoader/TerrainGasGiantLoader.cs",
        ])

    def can_install(self):
        return self.parser_src.output.exists() and self.source_dir.output.exists()

    def install(self):
        target_dir = self.game_dir.joinpath("GameData", "Kopernicus")
        rm_rf(target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "build", "GameData", "Kopernicus"), target_dir)

    def check_installed(self):
        target_dir = self.game_dir.joinpath("GameData", "Kopernicus")
        return target_dir.exists()
