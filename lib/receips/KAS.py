import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf


class Receipt:
    def __init__(self, game_dir, project_dir):
        self.game_dir = game_dir
        self.project_dir = project_dir
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Source" ))
        self.source_dir.output = project_dir.joinpath("Binaries", "KAS.dll")
        self.source_api_dir = SourceDir(game_dir, project_dir.joinpath("Source-API" ))
        self.source_api_dir.output = project_dir.joinpath("Binaries", "KAS-API-v1.dll")
        self.ksp_dev_lib = project_dir.parent.joinpath("KSPDev", "Binaries", "KSPDev_Utils.0.37.dll")
        self.target_dir = game_dir.joinpath("GameData", "KAS")

    def build(self):
        logging.info("  Build Release API")
        self.source_api_dir.std_compile(
            exclude="docs_project/**/*.cs",
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.ksp_dev_lib])
        logging.info("  Build Release")
        self.source_dir.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.ksp_dev_lib, self.source_api_dir.output])

    def install(self):
        rm_rf(self.target_dir)
        mkdir_p(self.target_dir)
        for sub_dir in ["Lang", "Models", "Parts", "Patches", "Sounds", "Textures"]:
            shutil.copytree(self.project_dir.joinpath(sub_dir), self.target_dir.joinpath(sub_dir))
        shutil.copy(self.project_dir.joinpath("settings.cfg"), self.target_dir)
        mkdir_p(self.target_dir.joinpath("Plugins"))
        shutil.copy(self.source_dir.output, self.target_dir.joinpath("Plugins"))
        shutil.copy(self.source_api_dir.output, self.target_dir.joinpath("Plugins"))
        shutil.copy(self.ksp_dev_lib, self.target_dir.joinpath("Plugins"))

    def check_installed(self):
        return self.target_dir.exists()
