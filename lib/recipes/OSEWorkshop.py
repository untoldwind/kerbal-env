import logging
import shutil
from lib.exec import run_command, SourceDir
from lib.utils import mkdir_p, rm_rf, rm
from lib.recipes import Receipt

class OSEWorkshop(Receipt):
    depends = ["ModuleManager", "KSPDev_Utils", "KIS", "FireSpitterCore", "CommunityResourcePack", "ClickThroughBlocker", "SpaceTuxLibrary"]

    def __init__(self, game_dir, project_dir):
        super().__init__(game_dir, project_dir)
        self.source_dir = SourceDir(game_dir, project_dir.joinpath("Workshop"))
        self.source_dir.output = project_dir.joinpath("GameData", "Workshop", "Plugins", "Workshop.dll")
        self.target_dir = game_dir.joinpath("GameData", "Workshop")
        self.clickthrouh_lib = project_dir.parent.joinpath("ClickThroughBlocker", "GameData", "000_ClickThroughBlocker", "Plugins", "ClickThroughBlocker.dll")
        self.ksp_dev_lib = project_dir.parent.joinpath("KSPDev_Utils", "Binaries", "KSPDev_Utils.2.0.dll")
        self.kis_lib = project_dir.parent.joinpath("KIS", "Binaries", "KIS.dll")
        self.ksp_log_lib = project_dir.parent.joinpath("SpaceTuxLibrary", "GameData", "SpaceTuxLibrary", "Plugins", "KSP_Log.dll")
        self.ksp_color_picker_lib = project_dir.parent.joinpath("SpaceTuxLibrary", "GameData", "SpaceTuxLibrary", "Plugins", "KSP_ColorPicker.dll")
        self.ksp_part_highlighter_lib = project_dir.parent.joinpath("SpaceTuxLibrary", "GameData", "SpaceTuxLibrary", "Plugins", "KSP_PartHighlighter.dll")
        self.toolbarcontrol_lib = project_dir.parent.joinpath("ToolbarControl", "GameData", "001_ToolbarControl", "Plugins", "ToolbarControl.dll")

    def build(self):
        logging.info("  Build Release")
        rm(self.project_dir.joinpath("GameData", "Workshop", "Plugins"), "*.dll")
        mkdir_p(self.project_dir.joinpath("GameData", "Workshop", "Plugins"));
        self.source_dir.std_compile(
            exclude="docs_project/**/*.cs",
            references=[self.kis_lib, self.clickthrouh_lib, self.ksp_dev_lib, self.ksp_log_lib,
                        self.ksp_color_picker_lib, self.ksp_part_highlighter_lib,
                        self.toolbarcontrol_lib,
                        "Assembly-CSharp.dll", 
                        "Assembly-CSharp-firstpass.dll", 
                        "UnityEngine.dll",
                        "UnityEngine.CoreModule.dll",
                        "UnityEngine.AnimationModule.dll",
                        "UnityEngine.IMGUIModule.dll",
                        "UnityEngine.TextRenderingModule.dll",
                        "UnityEngine.UI.dll"])

    def can_install(self):
        return self.source_dir.output.exists()

    def install(self):
        rm_rf(self.target_dir)
        shutil.copytree(self.project_dir.joinpath(
            "GameData", "Workshop"), self.target_dir)

    def check_installed(self):
        return self.target_dir.exists()
