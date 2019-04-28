import logging
import shutil
from lib.exec import SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt

class DockingPortAlignmentIndicator(Receipt):
    depends = ["ModuleManager"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.plugin_dir = project_dir.joinpath("GameData", "NavyFish", "Plugins", "Docking Port Alignment Indicator")
        self.source_dir1 = SourceDir(game_dir, project_dir.joinpath("Source", "DockingPortAlignmentIndicator", "ModuleDockingNodeNamed" ))
        self.source_dir1.output = self.plugin_dir.joinpath("ModuleDockingNodeNamed.dll")
        self.source_dir2 = SourceDir(game_dir, project_dir.joinpath("Source", "DockingPortAlignmentIndicator" ))
        self.source_dir2.output = self.plugin_dir.joinpath("DockingPortAlignmentIndicator.dll")
        self.source_dir3 = SourceDir(game_dir, project_dir.joinpath("Source", "DockingPortAlignmentIndicator", "DPAI_RPM" ))
        self.source_dir3.output = self.plugin_dir.joinpath("DPAI_RPM.dll")
        self.target_dir = game_dir.joinpath("GameData", "NavyFish")

    def build(self):
        logging.info("  Build Release")
        rm(self.plugin_dir, "*.dll")
        self.source_dir1.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll"])
        self.source_dir2.std_compile(
            exclude=[
                "DPAI_RPM/**/*",
                "ModuleDockingNodeNamed/**/*",
            ],
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.source_dir1.output])
        self.source_dir3.std_compile(
            references=["Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll", "UnityEngine.dll", "UnityEngine.UI.dll", self.source_dir1.output, self.source_dir2.output])

    def can_install(self):
        return self.source_dir1.output.exists() and self.source_dir2.output.exists() and self.source_dir3.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "NavyFish"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
