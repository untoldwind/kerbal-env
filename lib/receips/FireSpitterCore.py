import logging
import shutil
from lib.exec import SourceDir
from lib.utils import ln_s, rm_rf, rm, mkdir_p

class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Firespitter"))
        self.for_release_dir = self.project_dir.joinpath("For release", "Firespitter", "Plugins")
        self.source_dir.output = self.for_release_dir.joinpath("Firespitter.dll")
        self.target_dir = game_dir.joinpath("GameData", "Firespitter")

    def build(self):
        logging.info("  Build Release API")
        rm(self.for_release_dir, "*.dll")
        rm(self.for_release_dir, "*.mdb")
        rm(self.for_release_dir, "*.pdb")
        self.source_dir.std_compile(exclude="unused/*.cs|*Test.cs|FScrewTransfer.cs|FSattachPointUpdater.cs|FStoggleSurfaceAttach.cs",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        mkdir_p(self.target_dir)
        shutil.copytree(self.for_release_dir, self.target_dir.joinpath("Plugins"))
        shutil.copy(self.project_dir.joinpath("For release", "Firespitter", "Firespitter.version"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
