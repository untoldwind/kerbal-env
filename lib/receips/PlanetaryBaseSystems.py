import logging
import shutil
from lib.exec import SourceDir
from lib.utils import rm_rf, rm

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Sources", "PlanetarySurfaceStructures"))
        self.for_release_dir = self.project_dir.joinpath("FOR_RELEASE", "GameData", "PlanetaryBaseInc", "BaseSystem", "Plugins")
        self.source_dir.output = self.for_release_dir.joinpath("PlanetarySurfaceStructures.dll")
        self.target_dir = game_dir.joinpath("GameData", "PlanetaryBaseInc")

    def build(self):
        logging.info("  Build Release")
        rm(self.for_release_dir, "*.dll")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath("FOR_RELEASE", "GameData", "PlanetaryBaseInc"), self.target_dir)
        rm(self.target_dir.joinpath("ModSupport", "Parts", "KAS"), "*_LEGACY.cgf")

    def check_installed(self):
        return self.target_dir.exists()
