import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt

class OSEWorkshop(Receipt):
    depends = ["ModuleManager", "KIS", "FireSpitterCore", "CommunityResourcePack", "ClickThroughBlocker"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Workshop"))
        self.source_dir.output = project_dir.joinpath("GameData", "Workshop", "Plugins", "Workshop.dll")
        self.target_dir = game_dir.joinpath("GameData", "Workshop")
        self.clickthrouh_lib = project_dir.parent.joinpath("ClickThroughBlocker", "GameData", "000_ClickThroughBlocker", "ClickThroughBlocker.dll")
        self.kis_lib = project_dir.parent.joinpath("KIS", "Binaries", "KIS.dll")

    def build(self):
        logging.info("  Build Release")
        rm(self.project_dir.joinpath("GameData", "Workshop", "Plugins"), "*.dll")
        mkdir_p(self.project_dir.joinpath("GameData", "Workshop", "Plugins"));
        self.source_dir.std_compile(
            exclude="docs_project/**/*.cs",
            references=[self.kis_lib, self.clickthrouh_lib, "Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "Workshop"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
